import { useState, useRef, useEffect } from "react";
import "./DishChatbot.css";

type Message = {
    sender: "bot" | "user";
    text: string;
};

type Props = {
    dishId: string;
};

const DishChatbot = ({ dishId }: Props) => {
    const [messages, setMessages] = useState<Message[]>([
        {
            sender: "bot",
            text: "Hi 👋 I can help you understand this dish better. Ask me anything.",
        },
    ]);

    const [input, setInput] = useState("");
    const [stage, setStage] = useState<
        "chat" | "ask-feedback" | "collect-feedback" | "done"
    >("chat");

    const messagesEndRef = useRef<HTMLDivElement>(null);

    // -----------------------------
    // Auto scroll
    // -----------------------------
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    // -----------------------------
    // Send feedback to backend (RLHF)
    // -----------------------------
    const sendFeedbackToBackend = async (text: string) => {
        try {
            await fetch(`http://localhost:8000/menu/${dishId}/feedback`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text }),
            });
        } catch (err) {
            console.error("Feedback send failed", err);
        }
    };

    // -----------------------------
    // Send chat message (LLM + RAG)
    // -----------------------------
    const sendMessage = async () => {
        if (!input.trim()) return;

        const userQuestion = input.trim();
        setInput("");

        setMessages((prev) => [...prev, { sender: "user", text: userQuestion }]);

        try {
            const res = await fetch(
                `http://localhost:8000/menu/${dishId}/chat`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: userQuestion }),
                }
            );

            const data = await res.json();

            setMessages((prev) => [
                ...prev,
                { sender: "bot", text: data.text },
            ]);
        } catch {
            setMessages((prev) => [
                ...prev,
                {
                    sender: "bot",
                    text: "Sorry, I couldn’t fetch food insights right now.",
                },
            ]);
        }

        // Ask for feedback after 2 user questions
        setMessages((prev) => {
            const userCount = prev.filter(
                (m) => m.sender === "user"
            ).length;

            if (userCount === 2 && stage === "chat") {
                setTimeout(() => {
                    setMessages((p) => [
                        ...p,
                        {
                            sender: "bot",
                            text:
                                "Did this help you feel confident about this dish?",
                        },
                    ]);
                    setStage("ask-feedback");
                }, 400);
            }

            return prev;
        });
    };

    // -----------------------------
    // Feedback buttons (ALL lead to text)
    // -----------------------------
    const handleFeedbackChoice = (choice: string) => {
        setMessages((prev) => [
            ...prev,
            { sender: "user", text: choice },
            {
                sender: "bot",
                text:
                    "Thanks 🙏 Please write a short feedback so we can improve food safety insights.",
            },
        ]);

        setStage("collect-feedback");
    };

    // -----------------------------
    // Written feedback submission
    // -----------------------------
    const submitWrittenFeedback = () => {
        if (!input.trim()) return;

        const feedbackText = input.trim();
        setInput("");

        setMessages((prev) => [
            ...prev,
            { sender: "user", text: feedbackText },
            {
                sender: "bot",
                text: "Thank you for sharing your feedback 🙏",
            },
        ]);

        sendFeedbackToBackend(feedbackText);
        setStage("done");
    };

    return (
        <div className="chatbot">
            <div className="chat-messages">
                {messages.map((msg, i) => (
                    <div key={i} className={`chat-message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {stage === "chat" && (
                <div className="chat-input">
                    <input
                        placeholder="Ask about this dish..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) =>
                            e.key === "Enter" && sendMessage()
                        }
                    />
                    <button onClick={sendMessage}>Send</button>
                </div>
            )}

            {stage === "ask-feedback" && (
                <div className="feedback-buttons">
                    <button onClick={() => handleFeedbackChoice("👍 Yes")}>
                        👍 Yes
                    </button>
                    <button
                        onClick={() => handleFeedbackChoice("😐 Somewhat")}
                    >
                        😐 Somewhat
                    </button>
                    <button
                        onClick={() => handleFeedbackChoice("👎 Not really")}
                    >
                        👎 Not really
                    </button>
                </div>
            )}

            {stage === "collect-feedback" && (
                <div className="chat-input">
                    <input
                        placeholder="Write your feedback here..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) =>
                            e.key === "Enter" &&
                            submitWrittenFeedback()
                        }
                    />
                    <button onClick={submitWrittenFeedback}>
                        Submit
                    </button>
                </div>
            )}
        </div>
    );
};

export default DishChatbot;

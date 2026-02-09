import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import DishChatbot from "../components/DishChatbot";

import "./DishPage.css";

const DishDetailPage = () => {
    const { id } = useParams();
    const [dish, setDish] = useState<any>(null);
    const [insight, setInsight] = useState("");
    const [showInsight, setShowInsight] = useState(false);

    useEffect(() => {
        fetch(`https://ai-food-menu-backend.onrender.com/menu/${id}`)
            .then(res => res.json())
            .then(setDish);

        fetch(`https://ai-food-menu-backend.onrender.com/menu/${id}/insight`)
            .then(res => res.json())
            .then(data => setInsight(data.text));
    }, [id]);

    if (!dish) return <p className="loading">Loading...</p>;

    return (
        <div className="dish-page">
            {/* Hero Image */}
            <img
                src={`/images/${id}.jpeg`}
                alt={dish.name}
                className="dish-hero"
            />

            {/* Dish Info */}
            <div className="dish-info">
                <h1>{dish.name}</h1>

                <p className="dish-meta">
                    Category: {dish.category} ·{" "}
                    <span className={`status ${dish.status.toLowerCase()}`}>
                        {dish.status}
                    </span>
                </p>

                <p className="last-checked">
                    Last checked: {dish.last_checked}
                </p>

                {/* AI Insight Button */}
                <button
                    className="insight-btn"
                    onClick={() => setShowInsight(!showInsight)}
                >
                    🤖 AI Food Insight
                </button>

                {showInsight && (
                    <div className="ai-insight">
                        <p>
                            {insight || "Analyzing freshness and safety..."}
                        </p>
                    </div>
                )}

                {/* Chatbot */}
                <DishChatbot dishId={id!} />
            </div>
        </div>
    );
};

export default DishDetailPage;

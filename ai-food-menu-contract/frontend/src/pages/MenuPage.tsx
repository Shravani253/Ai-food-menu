import { useEffect, useState } from "react";
import MenuSection from "../components/MenuSection";
import type { MenuItem } from "../types/menu";
import "./MenuPage.css";   // 👈 THIS WAS MISSING

const MenuPage = () => {
    const [menu, setMenu] = useState<MenuItem[]>([]);

    useEffect(() => {
        fetch("https://ai-food-menu-backend.onrender.com/menu")
            .then(res => res.json())
            .then(data => setMenu(data))
            .catch(err => console.error("Menu fetch error:", err));
    }, []);

    const grouped = menu.reduce<Record<string, MenuItem[]>>((acc, item) => {
        if (!acc[item.category]) acc[item.category] = [];
        acc[item.category].push(item);
        return acc;
    }, {});

    return (
        <div className="menu-page">
            {/* Restaurant Header */}
            <header className="menu-title">
                <h1>Blue Tide Kitchen</h1>
                <p>AI-Powered Food Menu</p>
            </header>

            {/* Menu Sections */}
            {Object.entries(grouped).map(([category, items]) => (
                <MenuSection
                    key={category}
                    title={category}
                    items={items}
                />
            ))}
        </div>
    );
};

export default MenuPage;

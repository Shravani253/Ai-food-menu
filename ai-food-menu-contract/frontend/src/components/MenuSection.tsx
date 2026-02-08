import FoodCard from "./foodcard";
import type { MenuItem } from "../types/menu";
import "./MenuSection.css";

interface Props {
    title: string;
    items: MenuItem[];
}

const MenuSection = ({ title, items }: Props) => {
    return (
        <section className="menu-section">
            <h2>{title}</h2>

            <div className="horizontal-scroll">
                {items.map(item => (
                    <FoodCard key={item.id} item={item} />
                ))}
            </div>
        </section>
    );
};

export default MenuSection;

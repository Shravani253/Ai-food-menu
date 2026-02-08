import type { MenuItem } from "../types/menu";
import { Link } from "react-router-dom";
import "./FoodCard.css";

const FoodCard = ({ item }: { item: MenuItem }) => {
    return (
        <Link to={`/menu/${item.id}`} className="food-card-link">
            <div className="food-card">
                <img src={`/images/${item.id}.jpeg`} alt={item.name} />
                <div className="food-info">
                    <h4>{item.name}</h4>
                    <span className={`status ${item.status.toLowerCase()}`}>
                        {item.status}
                    </span>
                </div>
            </div>
        </Link>
    );
};

export default FoodCard;
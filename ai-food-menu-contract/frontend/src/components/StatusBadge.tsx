import type { Status } from "../types/menu";
import "./StatusBadge.css";

interface Props {
    status: Status;
}

export default function StatusBadge({ status }: Props) {
    return (
        <span className={`status-badge ${status.toLowerCase()}`}>
            {status}
        </span>
    );
}

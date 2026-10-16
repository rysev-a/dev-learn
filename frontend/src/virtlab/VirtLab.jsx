import EptLab from "./EptLab.jsx";
import HvLab from "./HvLab.jsx";
import MigrationLab from "./MigrationLab.jsx";
import NumaLab from "./NumaLab.jsx";
import Qcow2Lab from "./Qcow2Lab.jsx";
import VirtqLab from "./VirtqLab.jsx";
import "./virtlab.css";

/* Интерактивные упражнения книги «Виртуализация» (режим lab): симуляторы в браузере.
   Реестр: id упражнения → компонент. Решённое упражнение компонент сообщает через onSolved. */

const LABS = {
  "virt-sim-hv": HvLab,
  "virt-sim-ept": EptLab,
  "virt-sim-virtqueue": VirtqLab,
  "virt-sim-qcow2": Qcow2Lab,
  "virt-sim-migration": MigrationLab,
  "virt-sim-numa": NumaLab,
};

export const VIRT_LAB_IDS = Object.keys(LABS);

export default function VirtLab({ task, solved, onSolved }) {
  const Lab = LABS[task.id];
  if (!Lab) return <p className="empty">Упражнение не найдено</p>;
  return <Lab solved={solved} onSolved={onSolved} />;
}

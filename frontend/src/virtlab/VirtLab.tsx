import type { ComponentType } from "react";
import EptLab from "./EptLab.tsx";
import HvLab from "./HvLab.tsx";
import MigrationLab from "./MigrationLab.tsx";
import NumaLab from "./NumaLab.tsx";
import Qcow2Lab from "./Qcow2Lab.tsx";
import VirtqLab from "./VirtqLab.tsx";
import type { LabProps } from "./goals.ts";
import "./virtlab.css";

/* Интерактивные упражнения книги «Виртуализация» (режим lab): симуляторы в браузере.
   Реестр: id упражнения → компонент. Решённое упражнение компонент сообщает через onSolved. */

const LABS: Record<string, ComponentType<LabProps>> = {
  "virt-sim-hv": HvLab,
  "virt-sim-ept": EptLab,
  "virt-sim-virtqueue": VirtqLab,
  "virt-sim-qcow2": Qcow2Lab,
  "virt-sim-migration": MigrationLab,
  "virt-sim-numa": NumaLab,
};

export const VIRT_LAB_IDS = Object.keys(LABS);

export default function VirtLab({ task, solved, onSolved }: LabProps & { task: { id: string } }) {
  const Lab = LABS[task.id];
  if (!Lab) return <p className="empty">Упражнение не найдено</p>;
  return <Lab solved={solved} onSolved={onSolved} />;
}

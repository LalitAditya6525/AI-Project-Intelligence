import {
  HeartPulse,
  Target,
  PackageCheck,
  ShieldAlert,
  CircleAlert,
  FileText,
  PlusCircle,
} from "lucide-react";

const navigation = [
  { id: "health", label: "Health", icon: HeartPulse },
  { id: "scope", label: "Scope", icon: Target },
  {
    id: "deliverables",
    label: "Deliverables",
    icon: PackageCheck,
  },
  { id: "risk", label: "Risks", icon: ShieldAlert },
  { id: "blocker", label: "Blockers", icon: CircleAlert },
  {
    id: "documentation",
    label: "Documentation",
    icon: FileText,
  },
];

export default function Sidebar({
  activePage,
  onNavigate,
  onNewProject,
}) {
  return (
    <aside className="flex min-h-[calc(100vh-64px)] flex-col border-r border-slate-800 bg-[#0b1220] p-4">
      <p className="mb-5 px-3 text-xs font-semibold uppercase tracking-widest text-slate-500">
        Project Workspace
      </p>

      <nav className="space-y-2">
        {navigation.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => onNavigate(id)}
            className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-sm transition ${
              activePage === id
                ? "bg-indigo-500/15 text-indigo-300"
                : "text-slate-400 hover:bg-slate-800 hover:text-white"
            }`}
          >
            <Icon size={19} />
            <span>{label}</span>
          </button>
        ))}
      </nav>

      <div className="mt-auto border-t border-slate-800 pt-4">
        <button
          onClick={onNewProject}
          className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-sm text-indigo-300 transition hover:bg-indigo-500/10"
        >
          <PlusCircle size={19} />
          <span>New Project</span>
        </button>
      </div>
    </aside>
  );
}
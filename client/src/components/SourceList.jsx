import { FileText } from "lucide-react";

const SourceList = ({ sources = [] }) => {
  if (!sources.length) {
    return null;
  }

  return (
    <div className="mt-4">

      <p className="mb-2 text-xs font-medium uppercase tracking-wide text-slate-500">
        Sources
      </p>

      <div className="flex flex-wrap gap-2">

        {sources.map((source, index) => (
          <div
            key={`${source}-${index}`}
            className="
              flex items-center gap-2
              rounded-lg
              border border-slate-800
              bg-slate-900
              px-3 py-2
              text-xs text-slate-400
            "
          >
            <FileText size={14} />

            {source}
          </div>
        ))}

      </div>

    </div>
  );
};

export default SourceList;
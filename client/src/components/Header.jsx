function Header({
  title,
  project,
}) {

  return (
    <header className="sticky top-0 z-20 border-b border-gray-800 bg-[#0b0f17]/90 px-8 py-5 backdrop-blur">

      <div className="flex items-center justify-between">

        <div>

          <h2 className="text-xl font-semibold text-white">
            {title}
          </h2>

          <p className="mt-1 text-sm text-gray-600">
            {project?.name}
          </p>

        </div>


        <div className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-xs text-emerald-400">
          Analysis Complete
        </div>

      </div>

    </header>
  );
}

export default Header;
export const PageWrapper = ({ children }) => {
  return (
    <div className="w-full flex justify-center px-4">
      <div className="w-full max-w-[1376px]">{children}</div>
    </div>
  );
};

export const HomeCard = ({
  title,
  src,
  href,
  description,
}) => {
  return (
    <a
      href={href}
      className="mt-4 group flex flex-col overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm transition hover:shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 dark:border-zinc-800 dark:bg-zinc-900"
    >
      {/* Image (light/dark swap) */}
      <div className="relative w-full">
        <img src={src} alt={title} className="w-full object-cover" noZoom />
      </div>

      {/* Text area */}
      <div className="p-5">
        <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">{title}</h3>
        <p className="mt-1 text-sm leading-6 text-zinc-600 dark:text-zinc-400">{description}</p>
      </div>
    </a>
  );
};

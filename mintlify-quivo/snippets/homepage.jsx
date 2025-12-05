// File: homepage.jsx

export const HomeBanner = () => {
  return (
    <section className="w-full flex justify-center pt-8">
      {/* Updated to a two-column layout on medium screens and up */}
      <div className="max-w-[1376px] w-full flex flex-col md:flex-row items-center justify-between text-center md:text-left px-4 gap-8">

        {/* Left Column (Logo & Subtitle) */}
        <div className="max-w-2xl flex flex-col gap-10">
          {/* Logo */}
          <img noZoom src="/logo/light.svg"  className=" dark:hidden" />
          <img noZoom src="/logo/dark.svg" className=" hidden dark:block" />

          {/* Subtitle */}
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-300 max-w-2xl">
            
          </p>
        </div>

      </div>
    </section>
  );
};

export const PageWrapper = ({ children }) => {
  return (
    <div className="w-full flex justify-center px-4">
      <div className="w-full max-w-[1376px]">{children}</div>
    </div>
  );
};

// ADAPTED HomeCard Component:
// The class names are updated to match the original Quivo card design's border, shadow, and hover effect.
export const HomeCard = ({
  title = "Getting started",
  description = "Start utilizing the platform's features effectively.",
  href = "#",
  children,
  className = "", // Allow passing custom classes for specific cards
}) => {
  return (
    <a
      href={href}
      className={`block p-4 rounded-xl cursor-pointer transition duration-300 transform hover:scale-[1.02] bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 shadow-md hover:shadow-lg ${className}`}
    >
      {/* Image/Visual area - children will contain the custom visual for each card */}
      <div className="h-48 mb-4 bg-gray-100 dark:bg-zinc-800 rounded-lg overflow-hidden flex items-center justify-center relative">
        {children}
      </div>

      {/* Text area */}
      <div className="p-1"> {/* Padding adjusted to keep card text tighter to the bottom */}
        <h3 className="text-xl font-semibold mb-2 text-black dark:text-white">{title}</h3>
        {description && <p className="text-gray-600 dark:text-gray-400">{description}</p>}
      </div>
    </a>
  );
};
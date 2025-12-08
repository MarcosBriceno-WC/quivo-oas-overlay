export const HomeBanner = () => {
  return (
    <div className="w-full flex justify-center py-16">
      <div className="max-w-[1376px] w-full flex flex-col items-center text-center px-4">
        {/* Logo */}
        <img noZoom src="/images/homepage/logo.svg" alt="quivo Logo" className=" dark:hidden" />
        <img noZoom src="/images/homepage/darklogo.svg" alt="quivo Logo Dark" className=" hidden dark:block" />

        {/* Subtitle */}
        <p className="mt-4 text-lg text-gray-600 dark:text-gray-300 max-w-2xl">
          Dive into Our Docs and Start Building with Trusted, <br />
          AI-Powered Business Logic
        </p>
      </div>
    </div>
  );
};

import Trending from "./Trending"; // Import the Trending component

const HoverLinks = () => {
  return (
    <section className="bg-neutral-950 p-4 md:p-8 min-h-screen overflow-x-hidden">
      <div className="mx-auto max-w-5xl space-y-8">
        {/* Trending Section */}
        <Trending />

        {/* Other Links Section */}
        <div className="mx-auto max-w-3xl">
        </div>
      </div>
    </section>
  );
};

export default HoverLinks;

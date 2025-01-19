import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { useRef } from "react";

const Trending = () => {
  const ref = useRef<HTMLDivElement>(null);

  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const xSpring = useSpring(x);
  const ySpring = useSpring(y);

  const top = useTransform(ySpring, [0.5, -0.5], ["40%", "60%"]);
  const left = useTransform(xSpring, [0.5, -0.5], ["60%", "70%"]);

  const handleMouseMovement = (event: React.MouseEvent<HTMLDivElement>) => {
    if (ref.current) {
      const rectangle = ref.current.getBoundingClientRect();
      const width = rectangle.width;
      const height = rectangle.height;

      const mouseX = event.clientX - rectangle.left;
      const mouseY = event.clientY - rectangle.top;

      const xPercent = mouseX / width - 0.5;
      const yPercent = mouseY / height - 0.5;

      x.set(xPercent);
      y.set(yPercent);
    }
  };

  return (
    <motion.div
      ref={ref}
      onMouseMove={handleMouseMovement}
      className="relative m-auto w-full max-w-lg h-auto text-red-400 leading-7 rounded-[20px] bg-gray-700 p-5 shadow-lg hover:shadow-xl transition-shadow"
      initial={{ scale: 1, rotate: 0 }}
      whileHover={{ scale: 1.05, rotate: -5 }}
      transition={{ type: "spring", stiffness: 300 }}
    >
      <motion.h2
        initial={{ scale: 1 }}
        whileHover={{ scale: 1.1 }}
        className="text-[24px] border-b border-red-400 mb-4"
      >
        Trending💫
      </motion.h2>
      <ul className="space-y-4">
        {[
          { domain: "https://www.spotify.com", label: "www.spotify.com" },
          { domain: "https://www.applemusic.com", label: "www.applemusic.com" },
          { domain: "https://www.betting.com", label: "www.betting.com" },
        ].map((link, index) => (
          <motion.li
            key={index}
            initial="initial"
            whileHover="whileHover"
            variants={{
              initial: {
                x: 0,
                opacity: 1,
              },
              whileHover: {
                x: 10,
                opacity: 1,
              },
            }}
            className="hover:text-red-300 transition cursor-pointer"
          >
            <a
              href={link.domain}
              target="_blank"
              rel="noopener noreferrer"
              className="no-underline text-red-400"
            >
              {link.label}
            </a>
          </motion.li>
        ))}
      </ul>
      <motion.div
        variants={{
          initial: {
            x: "25%",
            opacity: 0,
          },
          whileHover: {
            x: "0%",
            opacity: 1,
          },
        }}
        transition={{
          type: "spring",
        }}
        className="relative z-10 p-4"
      >
        <span className="text-5xl text-neutral-500 group-hover:text-neutral-950 dark:group-hover:text-neutral-50">
          ➡️
        </span>
      </motion.div>
    </motion.div>
  );
};

export default Trending;

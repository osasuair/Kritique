import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { useRef } from "react";
import { FiArrowRight } from "react-icons/fi";

const Link = ({ heading, subheading, imgSrc, href }) => {
  const ref = useRef(null);

  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const xSpring = useSpring(x);
  const ySpring = useSpring(y);

  const top = useTransform(ySpring, [0.5, -0.5], ["40%", "60%"]);
  const left = useTransform(xSpring, [0.5, -0.5], ["60%", "70%"]);

  const handleMouseMovement = (event) => {
    const rectangle = ref.current.getBoundingClientRect();
    const width = rectangle.width;
    const height = rectangle.height;

    const mouseX = event.clientX - rectangle.left;
    const mouseY = event.clientY - rectangle.top;

    const xPercent = mouseX / width - 0.5;
    const yPercent = mouseY / height - 0.5;

    x.set(xPercent);
    y.set(yPercent);
  };

  return (
    <motion.a
      ref={ref}
      href={href}
      initial="initial"
      onMouseMove={handleMouseMovement}
      whileHover="whileHover"
      className="group relative flex items-center justify-between border-b-2 border-white dark:border-black py-4 transition-colors duration-500 hover:border-neutral-950 dark:hover:border-neutral-50 md:py-8 text-black dark:text-gray-500"
    >
      <div>
        <motion.span
          variants={{
            initial: {
              x: 0,
            },
            whileHover: {
              x: -16,
            },
          }}
          transition={{
            type: "spring",
            delayChildren: 0.25,
            staggerChildren: 0.075,
          }}
          className="relative z-10 block text-2xl font-bold text-gray-500 dark:text-gray-500 transition-colors duration-500 md:text-6xl group-hover:text-neutral-950 dark:group-hover:text-neutral-50"
        >
          {heading.split("").map((val, index) => (
            <motion.span
              variants={{
                initial: {
                  x: 0,
                },
                whileHover: {
                  x: 16,
                },
              }}
              transition={{
                type: "",
              }}
              className="inline-block"
              key={index}
            >
              {val}
            </motion.span>
          ))}
        </motion.span>
        <span className="relative z-10 mt-2 block text-gray-500 dark:text-gray-500 transition-colors duration-500 group-hover:text-neutral-950 dark:group-hover:text-neutral-50">
          {subheading}
        </span>
      </div>
      <motion.img
        variants={{
          initial: {
            scale: 0,
            rotate: "90deg",
          },
          whileHover: {
            scale: 1,
            rotate: "-20deg",
          },
        }}
        style={{
          top,
          left,
          translateX: "-50%",
          translateY: "-50%",
        }}
        transition={{
          type: "spring",
        }}
        src={imgSrc}
        className="absolute z-0 h-24 w-32 rounded-lg object-cover md:h-48 md:w-64"
        alt={`Image representing Link to ${heading}`}
      />

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
        <FiArrowRight className="text-5xl text-neutral-500 group-hover:text-neutral-950 dark:group-hover:text-neutral-50" />
      </motion.div>
    </motion.a>
  );
};

export default Link;

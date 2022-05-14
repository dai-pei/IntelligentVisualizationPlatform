import svelte from "rollup-plugin-svelte";
import commonjs from "@rollup/plugin-commonjs";
import resolve from "@rollup/plugin-node-resolve";
import serve from "rollup-plugin-serve";
import livereload from "rollup-plugin-livereload";
import { terser } from "rollup-plugin-terser";
import sveltePreprocess from "svelte-preprocess";
import typescript from "@rollup/plugin-typescript";
import css from "rollup-plugin-css-only";

const production = !process.env.ROLLUP_WATCH;
const smelte = require("smelte/rollup-plugin-smelte");

// function serve() {
//   let server;

//   function toExit() {
//     if (server) server.kill(0);
//   }

//   return {
//     writeBundle() {
//       if (server) return;
//       server = require("child_process").spawn("npm", ["run", "start:frontend"], {
//         stdio: ["ignore", "inherit", "inherit"],
//         shell: true,
//       });

//       process.on("SIGTERM", toExit);
//       process.on("exit", toExit);
//     },
//   };
// }

export default {
  input: "src/frontend/main.ts",
  output: {
    sourcemap: !production,
    format: "iife",
    name: "fluide",
    file: "public/build/bundle.js",
  },
  plugins: [
    smelte({
      purge: production,
      output: "public/global.css", // it defaults to static/global.css which is probably what you expect in Sapper
      postcss: [], // Your PostCSS plugins
      whitelist: [], // Array of classnames whitelisted from purging
      whitelistPatterns: [], // Same as above, but list of regexes
      tailwind: {
        theme: {
          extend: {
            spacing: {
              72: "18rem",
              84: "21rem",
              96: "24rem"
            }
          }
        }, // Extend Tailwind theme
        colors: {
          primary: "#b027b0",
          secondary: "#009688",
          error: "#f44336",
          success: "#4caf50",
          alert: "#ff9800",
          blue: "#2196f3",
          dark: "#212121"
        }, // Object of colors to generate a palette from, and then all the utility classes
        darkMode: true,
      }, // Any other props will be applied on top of default Smelte tailwind.config.js
    }),
    svelte({
      preprocess: sveltePreprocess({
          typescript: {
            tsconfigFile: production ? "./tsconfig.svelte.prod.json" : "./tsconfig.svelte.json",
          }
        }),
      compilerOptions: {
        // enable run-time checks when not in production
        dev: !production,
      },
    }),
    // we'll extract any component CSS out into
    // a separate file - better for performance
    css({
      output: "bundle.css",
      mangle: production ? true : false,
      compress: production ? true : false,
    }),

    // If you have external dependencies installed from
    // npm, you'll most likely need these plugins. In
    // some cases you'll need additional configuration -
    // consult the documentation for details:
    // https://github.com/rollup/plugins/tree/master/packages/commonjs
    resolve({
      browser: true,
      dedupe: ["svelte"],
    }),
    commonjs(),
    typescript({
      tsconfig: production ? "./tsconfig.svelte.prod.json" : "./tsconfig.svelte.json",
      sourceMap: !production,
      inlineSources: !production,
    }),

    // In dev mode, call `npm run start` once
    // the bundle has been generated
    !production &&
      serve({
        host: "localhost",
        port: 5000,
        contentBase: "public",
        // verbose: true,
      }),

    // Watch the `public` directory and refresh the
    // browser on changes when not in production
    !production &&
      livereload({
        watch: "public",
        // verbose: true,
      }),

    // If we're building for production (npm run build
    // instead of npm run dev), minify
    production &&
      terser({
        compress: true,
        mangle: true,
      }),
  ],
  watch: {
    clearScreen: false,
  },
};

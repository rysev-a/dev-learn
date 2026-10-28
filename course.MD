Creating a course for learning programming.
The main idea is that a user can walk the whole path in small steps by themselves, from studying discrete mathematics to writing a complex web service in Rust and JavaScript, learning all the necessary tools and technologies along the way.

Topics (order of the books in the left menu):

01. Discrete Mathematics
02. Python as a First Language
    - Language basics, functions, loops, data, classes, exceptions and files
    - Data model: special methods, operators, containers, descriptors
    - Iterators and generators (send/throw/yield from), functional programming
    - Metaprogramming: decorators, introspection, metaclasses, ast and dis
    - Standard library; class design: abc, protocols and generics, MRO
    - Asynchrony, Python internals (memory, GC, bytecode, GIL, performance)
    - Projects and tools: packages, uv, code quality, design patterns
03. Algorithms and Data Structures
    - using Python we go through all kinds of algorithms and data structures
04. Computer Architecture
05. From Assembler to C
    - the language only, without an OS
06. Diving into Unix
    - exercises in C
07. Computer Networks
08. Virtualization
09. Databases
10. Learning Rust
    - Basics
    - Core of the language
    - Data and abstractions
    - The language in depth
    - Algorithms
    - Architecture
    - Operating systems
    - A hand-written web server
    - A chat based on Axum, Sqlx, Tokio
11. Modern Frontend
    - History: the birth of JavaScript, Node.js and io.js, ES5 -> ES6, Babel, bundlers and preprocessors
    - Introduction to the JavaScript language (without a browser)
    - JavaScript in the browser: the engine and the event loop, DOM, CSS, events, network, Service Worker
    - JavaScript in Node.js
    - Bundlers (webpack, Vite, esbuild, Rollup), package managers, the npm and JSR registries, TypeScript
    - Our own mini-framework (we do not cover frameworks, algorithms have their own book)

Next in the plan: System Design. We build a full-fledged high-load service using CI/CD, e2e testing and all the patterns on gitlab, and deploy it to the cloud.

The end result: the user comes in, registers in the system and goes through the exercises step by step, sees their progress and can return to previous topics.

The exercises must be built so that the user cannot look up the answer, yet has no difficulty solving the task, because the difficulty grows very, very gradually, from the simplest to the hardest.

Say, at first the user studies Python and does many exercises on simple operations: addition, subtraction, multiplication and division, working with lists, dictionaries, sets, functions, classes, loops.

When the user reaches the Algorithms section, they no longer have questions about what a function, a loop or a dictionary is; they already know the basic data types and can even write simple algorithms, because they solved small tasks in the previous chapters, for example:

- find the sum of the elements in a list
- find the maximum element in a list
- find the minimum element in a list

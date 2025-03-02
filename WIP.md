# What is W.I.P. in PyBootstrapUI?

## Tauri Support  
Tauri is a modern framework for building lightweight, secure, and cross-platform desktop applications using Rust. It provides a robust set of tools and APIs, enabling developers to create applications that run seamlessly on Windows, Linux, and macOS. Tauri is known for its minimal resource usage and efficient performance, making it an excellent choice for building lightweight desktop applications.

## Electron Support  
Electron is a widely-used framework for building cross-platform desktop applications using web technologies like Chromium and Node.js. It offers a comprehensive set of APIs and tools, allowing developers to create applications that run on Windows, Linux, and macOS. However, Electron applications tend to be resource-intensive and are not considered lightweight, often requiring significant memory and processing power to run efficiently.

## Improved NW.js Support  
Currently, NW.js support in PyBootstrapUI is under development and somewhat unstable. NW.js (previously known as Node-WebKit) is a framework that enables developers to build desktop applications using HTML, CSS, and JavaScript. It combines the power of Node.js with the Chromium browser engine. Efforts are being made to streamline and enhance NW.js integration to provide a more stable and user-friendly experience.

---

## FastAPI Support  
As noted in the changelog for version 1.1.1, FastAPI support has been removed. FastAPI is a powerful framework for building high-performance APIs in Python, but it comes with a relatively heavy dependency footprint. In contrast, aiohttp is a more lightweight alternative, which aligns better with PyBootstrapUI's goal of minimizing dependencies and optimizing performance.

## Briefcase Support  
Briefcase is a tool for packaging Python applications into native executables for various platforms. It simplifies the process of distributing Python applications by generating installers for Windows, macOS, Linux, and more. Support for Briefcase is currently being explored to enhance PyBootstrapUI's ability to package and distribute applications seamlessly across multiple platforms.

## Code Obfuscation Before Building  
To safeguard developers' intellectual property, PyBootstrapUI is working on integrating automatic code obfuscation as part of the build process. This feature will help protect source code from reverse engineering and unauthorized access, ensuring that applications built with PyBootstrapUI remain secure.

---

These ongoing developments aim to expand PyBootstrapUI's capabilities, improve cross-platform compatibility, and provide developers with more tools to create efficient and secure applications.
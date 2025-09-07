# Docker LaTeX Container

This project provides a Docker container that uses pdflatex to compile LaTeX projects. LaTeX projects should be organized as subfolders within the [`ws_latex`](./ws_latex/) directory.

## Prerequisites

- Docker installed on your system.
- Basic knowledge of LaTeX document structure.

## Setup

Build the Docker container (Required only once or if [Dockerfile](./Dockerfile) is modified):
   ```bash
   ./scripts/build.sh
   ```

## Usage

### Basic Compilation

1. **Create your LaTeX project** in the [`ws_latex`](./ws_latex/) directory
    ```
    ws_latex/
    ├── your_project/
    │   ├── main.tex          # Main LaTeX file (required)
    │   ├── references.bib    # Bibliography file (optional)
    │   ├── images/           # Images directory (optional)
    │   └── ...              # Other LaTeX files
    ```
2. **Compile your project:**
   ```bash
   ./scripts/compile.sh your_project
   ```

## Examples

Compiling the test project:
```bash
./scripts/compile.sh test
```


## License

This project is licensed under a custom Academic/Personal Use License. See the [LICENSE](./LICENCE) file for details.

## Author

**Alejandro Daniel José Gómez Flórez**  
[LinkedIn](http://linkedin.com/in/aldajo92) | [GitHub](https://github.com/aldajo92)
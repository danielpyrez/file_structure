# 📂 File Structure Builder

A Python script that builds real folder and file structures from `.stru` files.  
It previews the tree with colors, supports text/binary content, asks for confirmation before applying changes, and can roll back errors—fast and safe project generation.  
**Bonus:** You can open `.stru` files directly by double-clicking the script.

## ✨ Features
- Colorful **tree preview** with [rich](https://github.com/Textualize/rich) + [colorama](https://pypi.org/project/colorama/).  
- Create folders and files directly from a `.stru` definition.  
- Embed **text** or **binary** content inside `.stru` files.  
- Confirmation step before applying changes.  
- **Rollback system** in case of errors.  
- Open `.stru` files directly with a double-click.

## 🔧 Usage
1. Create a `.stru` file describing your project structure.  
2. Run the script (or double-click it on Windows to open a `.stru` file).  
3. Preview the structure, confirm, and generate everything.

## 📄 Example `.stru`
```plaintext
#!structure
src
    main.py: print("Hello, world!")
docs
    README.md: */startwrite
    # Example Project
    */end

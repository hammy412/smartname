# SmartName Casing Guide

SmartName includes a **Casing & Preference Engine** that allows filenames to be formatted according to six different styles. This guide explains each style and provides examples.

---

## 1. Snake Case (`snake_case`) - Default

- **Description:** Words are lowercase and separated by underscores (`_`).  
- **Example:**  
  Input: `Simple Cartoon Duck`  
  Output: `simple_cartoon_duck`

---

## 2. Kebab Case (`kebab-case`)

- **Description:** Words are lowercase and separated by hyphens (`-`).  
- **Example:**  
  Input: `Simple Cartoon Duck`  
  Output: `simple-cartoon-duck`

---

## 3. Camel Case (`camelCase`)

- **Description:** The first word is lowercase, subsequent words are capitalized, with no spaces or separators.  
- **Example:**  
  Input: `Simple Cartoon Duck`  
  Output: `simpleCartoonDuck`

---

## 4. Pascal Case (`PascalCase`)

- **Description:** All words are capitalized, with no spaces or separators.  
- **Example:**  
  Input: `Simple Cartoon Duck`  
  Output: `SimpleCartoonDuck`

---

## 5. Lowercase With Spaces (`lowercase`)

- **Description:** All words are lowercase and separated by spaces.  
- **Example:**  
  Input: `Simple Cartoon Duck`  
  Output: `simple cartoon duck`

---

## 6. Title Case With Spaces (`TitleCase`)

- **Description:** All words are capitalized and separated by spaces.  
- **Example:**  
  Input: `Simple Cartoon Duck`  
  Output: `Simple Cartoon Duck`

---

## Usage in SmartName

When running SmartName, you can specify the casing style using the `--case` argument:

```bash
python rename_files.py ./data --case camelCase

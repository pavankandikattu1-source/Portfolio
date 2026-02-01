# Connect this repo to your GitHub profile

Your local Portfolio is already a Git repo with one commit. Follow these steps to link it to GitHub.

---

## 1. Create a new repository on GitHub

1. Go to **https://github.com/new**
2. **Repository name:** `Portfolio` (or e.g. `data-analyst-portfolio`)
3. **Description (optional):** e.g. "Data analyst portfolio – ING & Financial Services"
4. Choose **Public**
5. **Do not** add a README, .gitignore, or license (you already have these locally)
6. Click **Create repository**

---

## 2. Add GitHub as remote and push

In your terminal, from the Portfolio folder, run (replace **pavankandikattu1-source** with your GitHub username):

```bash
cd /Users/pavansatvik/Portfolio

# Add your new GitHub repo as the remote "origin"
git remote add origin https://github.com/pavankandikattu1-source/Portfolio.git

# Push your local main branch to GitHub
git push -u origin main
```

**Using SSH instead of HTTPS:**  
If you use SSH keys with GitHub, use:

```bash
git remote add origin git@github.com:pavankandikattu1-source/Portfolio.git
git push -u origin main
```

---

## 3. Check it’s connected

- Open **https://github.com/pavankandikattu1-source/Portfolio** in your browser — you should see your files.
- For future changes: `git add .` → `git commit -m "Your message"` → `git push`

---

## Optional: GitHub CLI (one-command setup later)

To create repos from the terminal in the future:

```bash
brew install gh
gh auth login
```

Then you could run something like `gh repo create Portfolio --public --source=. --push` from this folder (after the repo is created once, you’ll mainly use `git push`).

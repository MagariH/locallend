# LocalLend 🛠️📦
> **Hyper-local dorm & neighborhood resource sharing platform.**
> Borrow tools, appliances, and study gear from your dorm mates and neighbors instead of buying things you only use once.

Built for **Neighborhood Hacks**.

---

## 💡 The Problem
In college dormitories and apartment buildings, hundreds of residents own items they rarely use—drills, iron boards, vacuum cleaners, HDMI adapters, bike pumps, or textbooks. At the same time, next-door neighbors constantly need these exact items for 20 minutes, yet end up wasting money purchasing them new or going without.

## 🌟 Key Features
- **Dorm Resource Directory:** Browse available items categorized by tools, electronics, cleaning, kitchen appliances, and study essentials.
- **Instant Availability & Status:** Live tracking of item conditions and whether they are currently available or checked out.
- **One-Tap Lending Request:** Quick reservation system issuing a temporary pickup token to arrange contactless or room-to-room handover.
- **Community Trust Layer:** Simple rating and deposit-free accountability built specifically for student halls and local blocks.

---

## 🛠️ Built With
- **Python & FastAPI** — Asynchronous backend API handling inventory and reservation lifecycles
- **SQLite** — Lightweight database tracking items, users, and borrowing history
- **HTML5 & Tailwind CSS** — Clean, mobile-friendly interface designed for rapid dorm browsing
- **Vanilla JavaScript** — Real-time state updates without page reloads
- **Uvicorn** — High-performance ASGI application server

---

## 💻 How to Run Locally

Follow these quick steps to run the application on your computer:

**1. Install required dependencies:**
Open your terminal / command prompt and install the necessary Python packages:
```bash
pip install fastapi uvicorn pydantic
python -m uvicorn main:app --reload

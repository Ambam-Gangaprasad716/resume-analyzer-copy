from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

SKILLS = [
    "python", "java", "c", "html", "css",
    "flask", "sql", "ai", "data structures"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["GET"])
def analyze_page():
    return render_template("analyze.html")

@app.route("/resume/<page>")
def resume_pages(page):
    title = page.replace("-", " ").title()
    return render_template("pages/generic_content.html", title=f"Resume {title}", category="Resume")

@app.route("/resources/<page>")
def resources_pages(page):
    title = page.replace("-", " ").title()
    return render_template("pages/generic_content.html", title=f"Resources: {title}", category="Resources")

@app.route("/career/<page>")
def career_pages(page):
    title = page.replace("-", " ").title()
    return render_template("pages/generic_content.html", title=f"Career: {title}", category="Career Advice")

@app.route("/premium/pricing")
def premium_pricing():
    return render_template("pages/pricing.html")

@app.route("/faq")
def faq_page():
    return render_template("pages/faq.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return render_template("analyze.html", error="No file uploaded.")
        
    file = request.files["resume"]
    if file.filename == "":
        return render_template("analyze.html", error="No file selected.")
        
    if not file.filename.lower().endswith('.pdf'):
         return render_template("analyze.html", error="Only PDF files are supported.")

    text = ""

    try:
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text
    except Exception as e:
         return render_template("analyze.html", error=f"Error reading PDF: {str(e)}")
         
    if not text.strip():
        return render_template("analyze.html", error="Could not extract text from the PDF. It may be scanned or empty.")

    text_lower = text.lower()

    found_skills = []
    for skill in SKILLS:
        if skill in text_lower:
            found_skills.append(skill)

    score = len(found_skills) / len(SKILLS) * 100 if SKILLS else 0
    score = round(score)

    if score > 70:
        role = "Backend Developer"
    elif score > 40:
        role = "Junior Developer"
    else:
        role = "Beginner"

    return render_template(
        "analyze.html",
        text=text,
        skills=found_skills,
        score=score,
        role=role
    )

if __name__ == "__main__":
    app.run(debug=True)
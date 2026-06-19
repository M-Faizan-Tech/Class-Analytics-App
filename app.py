# pyright: reportMissingImports=false
from browser import document, bind, alert

# گلوبل سٹیٹ کنٹرول (اب سبجیکٹ کا نام اور اس کے ٹوٹل مارکس ڈکشنری میں ہوں گے)
subjects_dict = {"Math": 100, "Physics": 100, "Coding Lab": 50} 
students_list = []

def refresh_subject_ui():
    # ۱. بائیں طرف فارم میں ڈائنامک انپٹ باکس بنانا (ٹوٹل مارکس بھی لیبل میں دیکھیں گے)
    input_html = ""
    for sub, max_m in subjects_dict.items():
        input_html += f"""
        <div class="form-group">
            <label>{sub} Marks (Obtained / {max_m}):</label>
            <input type="number" class="dynamic-mark-input" data-subject="{sub}" max="{max_m}" placeholder="0-{max_m}">
        </div>
        """
    document["dynamic-subject-inputs"].innerHTML = input_html

    # ۲. سبجیکٹس کے اوپر نیلے رنگ کے چھوٹے ٹیگز دکھانا
    tag_html = ""
    for sub, max_m in subjects_dict.items():
        tag_html += f'<span class="subject-tag">📚 {sub} ({max_m})</span>'
    document["active-subjects-tags"].innerHTML = tag_html

    # ۳. دائیں طرف ٹیبل کے ہیڈرز کو اپڈیٹ کرنا
    header_html = "<th>Name</th>"
    for sub, max_m in subjects_dict.items():
        header_html += f"<th>{sub} ({max_m})</th>"
    header_html += "<th>Percentage</th><th>Grade</th>"
    document["table-headers"].innerHTML = header_html

def calculate_metrics():
    if not students_list or not subjects_dict:
        return

    table_rows = ""
    total_percentages = []
    
    # کل مارکس کا ٹوٹل نکالنا جو سبجیکٹس کے ایڈ ہونے پر بدل سکتا ہے
    max_possible = sum(subjects_dict.values())
    
    for s in students_list:
        total_obtained = sum(s["marks"].values())
        percentage = round((total_obtained / max_possible) * 100, 1)
        total_percentages.append(percentage)
        
        if percentage >= 90: grade = "A+"
        elif percentage >= 80: grade = "A"
        elif percentage >= 70: grade = "B"
        elif percentage >= 50: grade = "C"
        else: grade = "F"
        
        # ٹیبل روو بنانا
        row = f"<tr><td>{s['name']}</td>"
        for sub in subjects_dict.keys():
            row += f"<td>{s['marks'].get(sub, 0)}</td>"
        row += f"<td>{percentage}%</td><td><strong>{grade}</strong></td></tr>"
        table_rows += row
    
    document["student-rows"].innerHTML = table_rows

    # کلاس اوسط
    class_avg = sum(total_percentages) / len(total_percentages)
    
    # سورٹنگ
    sorted_students = sorted(zip(students_list, total_percentages), key=lambda x: x[1], reverse=True)
    
    # ٹاپ 3
    top_3_html = ""
    for i, (s, p) in enumerate(sorted_students[:3]):
        top_3_html += f"<li>🏅 Rank {i+1}: {s['name']} ({p}%)</li>"
    document["top-3-list"].innerHTML = top_3_html
    
    # لوسٹ سکورر
    lowest_student = sorted_students[-1]
    document["lowest-scorer"].innerHTML = f"❌ {lowest_student[0]['name']} ({lowest_student[1]}%)"
    
    # کیٹیگریز
    above_avg = []
    below_avg = []
    for s, p in sorted_students:
        if p >= class_avg:
            above_avg.append(s['name'])
        else:
            below_avg.append(s['name'])
            
    document["above-avg"].innerHTML = ", ".join(above_avg) if above_avg else "-"
    document["below-avg"].innerHTML = ", ".join(below_avg) if below_avg else "-"

# نیا سبجیکٹ اور اس کے مارکس ایڈ کرنے کا فنکشن
@bind(document["add-sub-btn"], "click")
def add_new_subject(event):
    sub_name = document["new-subject-name"].value.strip()
    sub_total = document["new-subject-total"].value
    
    if not sub_name or not sub_total:
        alert("Enter both Subject Name and Total Marks!")
        return
    if sub_name in subjects_dict:
        alert("Subject already exists!")
        return
        
    subjects_dict[sub_name] = int(sub_total)
    document["new-subject-name"].value = ""
    document["new-subject-total"].value = ""
    refresh_subject_ui()
    calculate_metrics()

# نیا سٹوڈنٹ ایڈ کرنے کا فنکشن
@bind(document["add-student-btn"], "click")
def add_student(event):
    name = document["student-name"].value.strip()
    if not name:
        alert("Please enter student name!")
        return
        
    inputs = document.select(".dynamic-mark-input")
    student_marks = {}
    
    for inp in inputs:
        sub = inp.attrs["data-subject"]
        max_m = subjects_dict[sub]
        val = inp.value
        
        if not val:
            alert(f"Please fill marks for {sub}!")
            return
        
        obtained = int(val)
        if obtained > max_m or obtained < 0:
            alert(f"Marks for {sub} must be between 0 and {max_m}!")
            return
            
        student_marks[sub] = obtained
        
    students_list.append({
        "name": name,
        "marks": student_marks
    })
    
    # فارم صاف کرنا
    document["student-name"].value = ""
    for inp in inputs:
        inp.value = ""
        
    calculate_metrics()

# ۵۰ فرضی سٹوڈنٹس کا ڈیٹا لوڈ کرنے کا فنکشن
@bind(document["demo-btn"], "click")
def load_massive_demo(event):
    global students_list
    students_list = []
    
    names = [
        "Ali", "Ayesha", "Zainab", "Usman", "Hamza", "Bilal", "Sana", "Zain", "Omer", "Fatima",
        "Muhammad", "Faizan", "Raza", "Amna", "Hassan", "Hussain", "Khadija", "Tayyaba", "Saad", "Anas",
        "Waqas", "Noman", "Asad", "Ibrahim", "Maryem", "Sara", "Yousaf", "Haris", "Fahad", "Zeeshan",
        "Kamran", "Daniyal", "Junaid", "Farhan", "Rizwan", "Siddique", "Kashif", "Adeel", "Salman", "Umair",
        "Arsalan", "Shahzaib", "Babar", "Imran", "Tariq", "Nabeel", "Ahsan", "Faisal", "Adnan", "Waseem"
    ]
    
    import random
    for i in range(50):
        marks_dict = {}
        for sub, max_m in subjects_dict.items():
            # خود بخود سلیکٹ کیے گئے میکسیمم مارکس کے رینج میں رینڈم نمبرز بنانا
            marks_dict[sub] = random.randint(int(max_m * 0.4), max_m) 
            
        students_list.append({
            "name": f"{names[i]} {random.choice(['Khan', 'Ahmed', 'Sheikh', 'Malik', 'Butt'])}",
            "marks": marks_dict
        })
        
    calculate_metrics()

# ایپ شروع ہوتے ہی یو آئی رینڈر کرنا
refresh_subject_ui()
def grade_task(score):
    """Convert Score into rubric Level"""
    grading_scale = {
        1: "🪨 Struggles",
        2: "🌿 Beginning",
        3: "🍁 Progressing",
        4: "🌳 Independent",
        5: "🌻 Mastery"
    }
    return grading_scale.get(score, "Not Assessed")

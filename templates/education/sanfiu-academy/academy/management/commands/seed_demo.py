from django.core.management.base import BaseCommand
from academy.models import Course, Lesson

COURSES = [
    {
        "title": "Designing with intention", "slug": "designing-with-intention", "category": "design", "level": "beginner",
        "summary": "A practical path from a rough idea to a clear, thoughtful interface.",
        "description": "Learn to turn a problem into a simple design direction. We will work through observation, hierarchy, color, type, and a small interface concept you can keep developing.",
        "instructor": "Mira Bennett", "estimated_hours": "2.5", "is_featured": True,
        "cover_image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=1400&q=85",
        "lessons": [
            ("Start with the problem", "start-with-the-problem", "Frame a useful design question before opening a design tool.", 12, True, "Good design begins with a clear question. Write down who you are designing for, what they need to do, and what currently gets in their way. Keep the first version specific and small."),
            ("Find the visual hierarchy", "find-the-visual-hierarchy", "Use scale and spacing to help people find their next step.", 18, False, "A page needs a clear first read. Choose one main message, one supporting detail, and one action. Give them different visual weight, then remove anything that competes with that order."),
            ("Build a small color system", "build-a-small-color-system", "Choose a palette that stays readable across the interface.", 20, False, "Start with a neutral background, a strong text color, and one accent. Check contrast at the sizes people will actually read. Add extra colors only when each one has a clear role."),
            ("Make a first screen", "make-a-first-screen", "Combine your decisions in a simple responsive landing page.", 24, False, "Sketch a headline, a short explanation, and the main action. Place them in a layout that still makes sense on a narrow screen. A good first screen tells people where they are and what to do next."),
        ],
    },
    {
        "title": "Python for everyday work", "slug": "python-for-everyday-work", "category": "technology", "level": "beginner",
        "summary": "Learn the building blocks of Python by automating small, useful tasks.",
        "description": "Get comfortable with variables, lists, loops, and functions through short examples. The lessons focus on reading and shaping everyday data, with a final script you can adapt to your own workflow.",
        "instructor": "Jonah Reed", "estimated_hours": "3.0", "is_featured": True,
        "cover_image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=1400&q=85",
        "lessons": [
            ("Your first Python script", "your-first-python-script", "See how a small script receives input and produces output.", 14, True, "A Python script is a set of instructions that run from top to bottom. Try changing a print statement and run the file again. Small edits are the fastest way to learn what each line does."),
            ("Store and shape information", "store-and-shape-information", "Use names, strings, numbers, and lists to represent information.", 22, False, "Variables give useful names to values. Lists group related values together. Choose names that describe the information so your future self can understand the script without guessing."),
            ("Repeat work with a loop", "repeat-work-with-a-loop", "Process each item in a list without copying the same lines.", 20, False, "A for loop runs the same block for each item in a collection. Keep the repeated work inside the loop and use the current item where needed. Indentation shows which instructions belong to it."),
            ("Turn steps into a function", "turn-steps-into-a-function", "Give a useful block of work a name and reuse it.", 24, False, "Functions help you package a repeated task. Give the function a clear name, accept the information it needs as parameters, and return the result so another part of the program can use it."),
        ],
    },
    {
        "title": "A calmer weekly plan", "slug": "a-calmer-weekly-plan", "category": "wellbeing", "level": "intermediate",
        "summary": "Make a flexible plan that leaves room for focused work and real breaks.",
        "description": "Build a planning routine around your actual energy and responsibilities. This short course covers priorities, time blocks, buffers, and a weekly review you can keep lightweight.",
        "instructor": "Leila Morgan", "estimated_hours": "1.5", "is_featured": False,
        "cover_image_url": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1400&q=85",
        "lessons": [
            ("Choose what matters this week", "choose-what-matters-this-week", "Separate important outcomes from the noise of a long task list.", 11, True, "Write down everything asking for your attention. Circle the outcomes that would make the week feel useful. Keep the list short enough that your time and energy can reasonably support it."),
            ("Give work a realistic home", "give-work-a-realistic-home", "Use flexible blocks and leave space for interruptions.", 16, False, "Estimate the time a task needs, then give it a block with a little room around it. A plan is a guide, not a promise that every day will go exactly as expected."),
            ("Review and reset", "review-and-reset", "Close the week by noticing what worked and adjusting gently.", 13, False, "At the end of the week, note what moved forward, what took longer, and what can wait. Carry only the useful lessons into the next plan."),
        ],
    },
]

class Command(BaseCommand):
    help = "Create or update the sample courses and lessons."

    def handle(self, *args, **options):
        for item in COURSES:
            course_data = item.copy()
            lesson_data = course_data.pop("lessons")
            course, _ = Course.objects.update_or_create(slug=course_data["slug"], defaults={**course_data, "is_published": True})
            for position, (title, slug, summary, duration, is_preview, content) in enumerate(lesson_data, start=1):
                Lesson.objects.update_or_create(
                    course=course, slug=slug,
                    defaults={"title": title, "summary": summary, "duration_minutes": duration,
                              "is_preview": is_preview, "content": content, "position": position, "is_published": True},
                )
        self.stdout.write(self.style.SUCCESS("Sample courses and lessons are ready."))

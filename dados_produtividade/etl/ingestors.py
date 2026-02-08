import pandas as pd
import numpy as np
from datetime import timedelta
from django.utils import timezone
from dados_produtividade.models import ActivityLog, Category, Source, Task

class MockIngestor:
    def __init__(self):
        self.sources = ["WakaTime", "Manual", "Calendar"]
        self.categories = [
            ("Coding", True, "#007bff"), 
            ("Meeting", False, "#dc3545"), 
            ("Writing", True, "#ffc107"),
            ("Break", False, "#28a745")
        ]

    def setup_master_data(self):
        # Create Sources
        for name in self.sources:
            Source.objects.get_or_create(name=name)
        
        # Create Categories
        for name, productive, color in self.categories:
            Category.objects.get_or_create(name=name, defaults={"is_productive": productive, "color": color})

    def generate_data(self, days=30):
        self.setup_master_data()
        
        # Generate logs
        print(f"Generating data for last {days} days...")
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        cats = list(Category.objects.all())
        srcs = list(Source.objects.all())
        
        current = start_date
        count = 0
        while current < end_date:
            # Random duration between 15 min and 3 hours
            duration_mins = np.random.randint(15, 180) 
            duration = timedelta(minutes=duration_mins)
            
            log_end = current + duration
            if log_end > end_date:
                break
                
            cat = cats[np.random.randint(0, len(cats))]
            src = srcs[np.random.randint(0, len(srcs))]
            
            log = ActivityLog(
                start_time=current,
                end_time=log_end,
                description=f"Activity: {cat.name} via {src.name}",
                category=cat,
                source=src
            )
            log.save() # Call save to calc duration
            count += 1
            
            # Gap between tasks
            gap = timedelta(minutes=np.random.randint(5, 60))
            current = log_end + gap
            
        print(f"Data generation complete. {count} logs created.")

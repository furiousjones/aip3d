class PrintJob:
    def __init__(self, model, settings):
        self.model = model
        self.settings = settings

class QueueManager:
    def __init__(self):
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)

    def list_jobs(self):
        return self.jobs

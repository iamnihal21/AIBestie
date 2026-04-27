# Add these two lines to BestieAssistant.__init__() after existing tool setup:

        # Wire up Scheduler so reminders actually fire
        from core.scheduler import Scheduler
        self.scheduler = Scheduler(self.speaker)
        self.scheduler.start()

class File:
    def __init__(self, file_name, file_type, file_size, creation_date, slack_space_data=None):
        self.file_name = file_name
        self.file_type = file_type
        self.file_size = file_size
        self.creation_date = creation_date
        self.slack_space_data = slack_space_data  # Slack space or unallocated space data

    def __repr__(self):
        return (f"File: {self.file_name}\n"
                f"Type: {self.file_type}\n"
                f"Size: {self.file_size} bytes\n"
                f"Creation Date: {self.creation_date}\n"
                f"Slack Space: {self.slack_space_data if self.slack_space_data else 'No data'}")

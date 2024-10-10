class File:
    def __init__(self, file_type, starting_offset, ending_offset, filepath):
        self.file_type = file_type
        self.starting_offset = starting_offset  # Starting offset in the original file
        self.ending_offset = ending_offset      # Ending offset in the original file
        self.filepath = filepath                # Path where the file is located

    def __repr__(self):
        return (
                f"Type: {self.file_type}\n"
                f"Starting Offset: {self.starting_offset}\n"
                f"Ending Offset: {self.ending_offset}\n"
                f"File Path: {self.filepath}\n"
                )


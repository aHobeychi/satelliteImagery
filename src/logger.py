"""
Logger class is used to write the results to a file withouth having to worry
about it.
"""
from pathlib import Path
import project_manager


class Logger():
    """Class to log the results and useful information"""
    def __init__(self):
        self.output_path = project_manager.logging_path + 'log.csv'
        self.packet = self.Packet()

        if not Path(self.output_path).is_file():
            with open(self.output_path, 'a') as log_file:
                log_file.write('project,date,image_type,clusters,cropped' +
                               ',normalized,algorithm,cost\n')

    def log(self, *information):
        """
        logs information and add it to the packet.
        The standard format of the message is the following:
        project,date,image_type,clusters,cropped,normalized,algorithm,cost.
        """
        for info in information:
            self.packet.append_packet(str(info))

    def push_information(self):
        """
        Writes the packet to the file and Purges the packet
        """
        with open(self.output_path, 'a') as log_file:
            log_file.write(self.packet.get_packet(True)[:-1] + '\n')
            log_file.close()

    class Packet():
        """
        Class that contains each packet that will be written to a file
        """
        def __init__(self):
            self.packet = ''

        def append_packet(self, information):
            """
            Appends packet with information followed by a space
            """
            self.packet += '{},'.format(information)

        def purge_packet(self):
            """
            Resets the packet to the empty string.
            """
            self.packet = ''

        def get_packet(self, purge=False):
            """
            Return the packet, if purge is True will delete the message.
            """
            tmp = self.packet
            if purge:
                self.purge_packet()
            return tmp

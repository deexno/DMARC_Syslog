import gzip
import io
import zipfile

from lxml import etree

from logger import ExceptlogClient


class Utility:
    @staticmethod
    def decompress_gz_to_byte(compressed_content):
        try:
            # Attempt to decompress the gzip-compressed content
            tmp = gzip.decompress(compressed_content)
            return tmp
        except Exception as exception:
            # If an exception occurs, log it using the ExceptlogClient and
            # return None
            ExceptlogClient.log_except(exception)
            return None

    @staticmethod
    def decompress_zip_to_byte(compressed_content):
        try:
            # Open the zip file using ZipFile and read the contents of the
            # first file in the archive
            tmp = zipfile.ZipFile(io.BytesIO(compressed_content))
            extracted_file = tmp.read(tmp.infolist()[0])
            tmp.close()

            return extracted_file
        except Exception as exception:
            # If an exception occurs, log it using the ExceptlogClient and
            # return None
            ExceptlogClient.log_except(exception)
            return None

    @staticmethod
    def byte_to_xml(byte_content):
        # Parse the byte content as XML using the lxml library
        return etree.XML(byte_content)

    @staticmethod
    def xml_to_string(xml):
        # Convert the XML object to a string representation
        return etree.tostring(xml, encoding="utf8").decode("utf8")

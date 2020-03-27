import struct
from src.tools import serialize


class CandidateVotes(object):

    def __init__(self, candidate: bytes, votes: int):
        self.candidate = candidate
        self.votes = votes

    def serialize(self, version: int):
        r = b""
        r = serialize.write_var_bytes(r, self.candidate)
        r += struct.pack("<q", self.votes)
        return r

    def deserialize(self, version: int):
        pass

    def __repr__(self):
        return "VoteContent {\n\t" \
               + "candidate: {}".format(self.candidate.hex()) + "\n" \
               + "votes: {}".format(self.votes) + "\n\t" \
               + "}"

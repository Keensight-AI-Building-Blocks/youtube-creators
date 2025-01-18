from fastapi import HTTPException


class TranscriptLoadError(HTTPException):
    def __init__(self, detail: str = "Error loading transcript"):
        super().__init__(status_code=500, detail=detail)


class QueryError(HTTPException):
    def __init__(self, detail: str = "Error processing query"):
        super().__init__(status_code=500, detail=detail)


class AnalyzeCommentsError(HTTPException):
    def __init__(self, detail: str = "Error analyzing comments"):
        super().__init__(status_code=500, detail=detail)


class GenerateVideoIdeasError(HTTPException):
    def __init__(self, detail: str = "Error generating video ideas"):
        super().__init__(status_code=500, detail=detail)

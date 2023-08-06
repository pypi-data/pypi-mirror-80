import fastapi
import starlette.responses

from . import parser

router = fastapi.APIRouter(default_response_class=starlette.responses.UJSONResponse)
router.include_router(parser.router, prefix="/parser")

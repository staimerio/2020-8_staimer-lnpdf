# Retic
from retic import Request, Response, Next

# Services
import services.wordpress.wordpress as wordpress
from retic.services.validations import validate_obligate_fields
from retic.services.responses import success_response_service, error_response_service


def create_post(req: Request, res: Response, next: Next):
    """Create a new post"""

    """Validate obligate params"""
    _validate = validate_obligate_fields({
        u'title': req.param('title'),
    })

    """Check if has errors return a error response"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response_service(
                "The param {} is necesary.".format(_validate["error"])
            )
        )

    _post = wordpress.create_post(
        title=req.param('title'),
        slug=req.param('slug', None),
        content=req.param('content', ""),
        excerpt=req.param('excerpt', ""),
        categories=req.param('categories', []),
        tags=req.param('tags', []),
        types=req.param('types', []),
        genres=req.param('genres', []),
        meta=req.param('meta', []),
        date=req.param('date', ""),
    )

    """Check if it has any problem"""
    if _post['valid'] is False:
        res.bad_request(_post)
    else:
        res.ok(_post)


def update_post(req: Request, res: Response, next: Next):
    """Update a post"""

    """Validate obligate params"""
    _validate = validate_obligate_fields({
        u'post_id': req.param('post_id'),
        u'data': req.param('data'),
    })

    """Check if has errors return a error response"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response_service(
                "The param {} is necesary.".format(_validate["error"])
            )
        )

    _post = wordpress.update_post(
        post_id=req.param('post_id'),
        data=req.param('data'),
    )

    """Check if it has any problem"""
    if _post['valid'] is False:
        res.bad_request(_post)
    else:
        res.ok(
            success_response_service(
                data=_post['data'],
                msg="Post updated."
            )
        )


def get_post_by_id(req: Request, res: Response, next: Next):
    """Get a post"""

    _post = wordpress.get_post_by_id(
        post_id=req.param('post_id'),
    )

    """Check if it has any problem"""
    if _post['valid'] is False:
        res.bad_request(_post)
    else:
        res.ok(
            success_response_service(
                data=_post['data'],
                msg='Post found.'
            )
        )


def get_all_search(req: Request, res: Response):
    if req.param('slug'):
        return get_by_slug(req, res)
    return res.bad_request("Bad request")


def get_by_slug(req: Request, res: Response):
    """Get all novel from latests page"""
    _post = wordpress.get_post_by_slug(
        slug=req.param('slug')
    )
    """Check if exist an error"""
    if _post['valid'] is False:
        return res.not_found(_post)
    else:
        """Response the data to client"""
        res.ok(
            success_response_service(
                data=_post['data'],
                msg='Post found.'
            )
        )

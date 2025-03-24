from app import setup_keys, sdx_app
from app.routes import deliver_dap, deliver_legacy, deliver_hybrid, deliver_feedback, deliver_comments, deliver_seft
from app.v2.routes import deliver_business_survey, deliver_adhoc_survey, deliver_comments_file, deliver_seft_submission

if __name__ == '__main__':
    setup_keys()

    sdx_app.add_post_endpoint(deliver_dap, rule="/deliver/dap")
    sdx_app.add_post_endpoint(deliver_legacy, rule="/deliver/legacy")
    sdx_app.add_post_endpoint(deliver_hybrid, rule="/deliver/hybrid")
    sdx_app.add_post_endpoint(deliver_feedback, rule="/deliver/feedback")
    sdx_app.add_post_endpoint(deliver_comments, rule="/deliver/comments")
    sdx_app.add_post_endpoint(deliver_seft, rule="/deliver/seft")

    sdx_app.add_post_endpoint(deliver_business_survey, rule="/deliver/v2/business")
    sdx_app.add_post_endpoint(deliver_adhoc_survey, rule="/deliver/v2/adhoc")
    sdx_app.add_post_endpoint(deliver_comments_file, rule="/deliver/v2/comments")
    sdx_app.add_post_endpoint(deliver_seft_submission, rule="/deliver/v2/seft")

    sdx_app.run(port=5000)

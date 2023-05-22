from app import setup_keys, sdx_app
from app.routes import deliver_dap, deliver_legacy, deliver_hybrid, deliver_feedback, deliver_comments, deliver_seft

if __name__ == '__main__':
    setup_keys()

    sdx_app.add_post_endpoint(deliver_dap, rule="/deliver/dap")
    sdx_app.add_post_endpoint(deliver_legacy, rule="/deliver/legacy")
    sdx_app.add_post_endpoint(deliver_hybrid, rule="/deliver/hybrid")
    sdx_app.add_post_endpoint(deliver_feedback, rule="/deliver/feedback")
    sdx_app.add_post_endpoint(deliver_comments, rule="/deliver/comments")
    sdx_app.add_post_endpoint(deliver_seft, rule="/deliver/seft")

    sdx_app.run(port=5000)

import logging

default_log = logging.getLogger(__name__)
st = logging.StreamHandler()
default_log.setLevel(logging.INFO)
fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s ")
st.setFormatter(fmt)
default_log.addHandler(st)


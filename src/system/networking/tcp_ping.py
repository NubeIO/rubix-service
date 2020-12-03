"""
TCP Ping Test
"""

import socket
import time
from timeit import default_timer as timer


def tcpping(d_host, d_port=80, maxCount=10, DEBUG=False):
    """ Default to port 80 and count of 10 """
    # Pass/Fail counters
    COUNT = 0
    PASSED = 0
    FAILED = 0
    _avg_timer = 0

    while COUNT < maxCount:
        # Increment Counter
        COUNT += 1
        success = False
        # New Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 1sec Timeout
        s.settimeout(1)
        # Start a timer
        s_start = timer()
        # Try to Connect
        try:
            s.connect((d_host, int(d_port)))
            s.shutdown(socket.SHUT_RD)
            success = True
        # Connection Timed Out
        except socket.timeout:
            if DEBUG:
                print("Connection timed out!")
            FAILED += 1
        except OSError as e:
            if DEBUG:
                print("OS Error:", e)
            FAILED += 1
        # Stop Timer
        s_stop = timer()
        s_runtime = "%.2f" % (1000 * (s_stop - s_start))
        _avg_timer = _avg_timer + float(s_runtime)

        if success:
            if DEBUG:
                print("Connected to %s[%s]: tcp_seq=%s time=%s ms" % (d_host, d_port, (COUNT - 1), s_runtime))
            PASSED += 1

        # Sleep for 1sec
        if COUNT < maxCount:
            time.sleep(0.1)

    ### Summarize and return Results
    lRate = 0
    AVG = _avg_timer / COUNT
    if FAILED != 0:
        lRate = FAILED / (COUNT) * 100
        lRate = "%.2f" % lRate
    if COUNT:  ### FIXME
        print("\nTCP Ping Results: Connections (Total/Pass/Fail/Avg): [{:}/{:}/{:}/{:}] (Failed: {:}%)".format(
            (COUNT), PASSED, FAILED, round(AVG, 3), str(lRate)))

    return {'d_host': d_host, 'd_port': d_port, 'count': COUNT, 'passed': PASSED, 'failed': FAILED,
            'average': round(AVG, 3), 'lost_rate': lRate}


# Dummy destination for local test
if __name__ == "__main__":
    tcpping(d_host='192.168.0.102', d_port=502, maxCount=10, DEBUG=True)

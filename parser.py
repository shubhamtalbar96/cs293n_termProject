import json as js
import csv
import glob

# set of all the features
header = ['remote_inbound_jitter', 'remote_packetsLost/s', 'remote_fractionLost',
          # 'inbound_jitter', 'inbound_packetsLost', 'inbound_packetsReceived/s', 'inbound_framesReceived/s',
          # 'inbound_frameWidth', 'inbound_frameHeight', 'inbound_framesPerSecond', 'inbound_framesDropped',
          # 'inbound_totalInterFrameDelay/framesDecoded_in_ms', 'inbound_firCount',
          # 'inbound_pliCount', 'inbound_nackCount', 'inbound_qpSum/framesEncoded',
          # 'inbound_bytesReceived/s',
          'outbound_packetsSent/s', 'outbound_frameWidth', 'outbound_frameHeight',
          'outbound_framesPerSecond', 'outbound_framesSent/s',
          'outbound_totalPacketSentDelay/packetsSent_in_ms', 'outbound_firCount/s',
          # 'outbound_pliCount',
          'outbound_bytesSent/s', 'outbound_nackCount/s', 'outbound_qpSum/framesEncoded'
          ]


def preprocess(input_key, data_type=0):
    temp_string = input_key[1]['values']
    temp_string = temp_string.split(']')
    temp_string = temp_string[0].split('[')
    temp_string = temp_string[1]

    if data_type == 0:
        feature_vector = [int(s) for s in temp_string.split(',')]
    else:
        feature_vector = [float(s) for s in temp_string.split(',')]
    return feature_vector


def parse_directory(ip_directory_path, op_directory_path):
    file_names = glob.glob(ip_directory_path + "*/*.txt")
    # file_names = glob.glob(ip_directory_path + "*.txt")

    for file_name in file_names:
        print("processing file_name = " + file_name)

        file_name_split = file_name.split('/')
        json_file_split = file_name_split[-1].split('.')
        output_file_path = op_directory_path + file_name_split[-2] + '_' + json_file_split[0] + "_features" + ".csv"

        parse_file(file_name, output_file_path)


def parse_file(file_path, output_file_path):
    f = open(file_path, "r")
    json_string = f.read()
    f.close()

    json = js.loads(json_string)

    remote_inbound_jitter = None
    remote_packetsLost_per_sec = None
    remote_fractionLost = None

    # inbound_jitter = None
    # inbound_packetsLost = None
    # inbound_packetsReceived_per_sec = None
    # inbound_framesReceived_per_sec = None
    # inbound_frameWidth = None
    # inbound_frameHeight = None
    # inbound_framesPerSecond = None
    # inbound_framesDropped = None
    # inbound_totalInterFrameDelay_framesDecoded_in_ms = None
    # inbound_firCount = None
    # inbound_pliCount = None
    # inbound_nackCount = None
    # inbound_qpSum_framesDecoded = None
    # inbound_bytesReceived_per_sec = None

    outbound_packetsSent_per_sec = None
    outbound_frameWidth = None
    outbound_frameHeight = None
    outbound_framesPerSecond = None
    outbound_framesSent_per_sec = None
    outbound_totalPacketSendDelay_packetsSent_in_ms = None
    outbound_firCount_per_sec = None
    # outbound_pliCount = None
    outbound_bytesSent_per_sec = None
    outbound_nackCount_per_sec = None
    outbound_qpSum_framesEncoded = None

    for peer_connection in json["PeerConnections"]:
        peer_connection_value = json["PeerConnections"][peer_connection]
        peer_stats = peer_connection_value["stats"]

        for key in peer_stats.items():
            key_name = key[0]
            if "RTCOutboundRTPVideoStream" in key_name:
                if key_name.find("packetsSent/s") != -1:
                    outbound_packetsSent_per_sec = preprocess(key,1 )
                elif key_name.find("frameWidth") != -1:
                    outbound_frameWidth = preprocess(key,1 )
                elif key_name.find("frameHeight") != -1:
                    outbound_frameHeight = preprocess(key,1 )
                elif key_name.find("framesPerSecond") != -1:
                    outbound_framesPerSecond = preprocess(key,1 )
                elif key_name.find("framesSent/s") != -1:
                    outbound_framesSent_per_sec = preprocess(key,1 )
                elif key_name.find("totalPacketSendDelay/packetsSent_in_ms") != -1:
                    outbound_totalPacketSendDelay_packetsSent_in_ms = preprocess(key,1 )
                elif key_name.find("firCount") != -1:
                    outbound_firCount_per_sec = preprocess(key,1 )
                # elif key_name.find("pliCount") != -1:
                #     outbound_pliCount = preprocess(key,1 )
                elif key_name.find("bytesSent_in_bits/s") != -1:
                    outbound_bytesSent_per_sec = preprocess(key,1 )
                elif key_name.find("nackCount") != -1:
                    outbound_nackCount_per_sec = preprocess(key,1 )
                elif key_name.find("qpSum/framesEncoded") != -1:
                    outbound_qpSum_framesEncoded = preprocess(key,1 )

            elif "RTCRemoteInboundRtpVideoStream" in key_name:
                if key_name.find("jitter") != -1:
                    remote_inbound_jitter = preprocess(key,1 )
                elif key_name.find("packetsLost") != -1:
                    remote_packetsLost_per_sec = preprocess(key,1 )
                elif key_name.find("fractionLost") != -1:
                    remote_fractionLost = preprocess(key,1 )

            # elif "RTCInboundRTPVideoStream" in key_name:
            #     if key_name.find("-jitter") != -1 and key_name[-1] == 'r':
            #         inbound_jitter = preprocess(key, 1)
            #     elif key_name.find("packetsLost") != -1:
            #         inbound_packetsLost = preprocess(key, 1)
            #     elif key_name.find("packetsReceived/s") != -1:
            #         inbound_packetsReceived_per_sec = preprocess(key, 1)
            #     elif key_name.find("framesReceived/s") != -1:
            #         inbound_framesReceived_per_sec = preprocess(key, 1)
            #     elif key_name.find("frameWidth") != -1:
            #         inbound_frameWidth = preprocess(key, 1)
            #     elif key_name.find("frameHeight") != -1:
            #         inbound_frameHeight = preprocess(key, 1)
            #     elif key_name.find("framesPerSecond") != -1:
            #         inbound_framesPerSecond = preprocess(key, 1)
            #     elif key_name.find("framesDropped") != -1:
            #         inbound_framesDropped = preprocess(key, 1)
            #     elif key_name.find("totalInterFrameDelay/framesDecoded_in_ms") != -1:
            #         inbound_totalInterFrameDelay_framesDecoded_in_ms = preprocess(key, 1)
            #     elif key_name.find("firCount") != -1:
            #         inbound_firCount = preprocess(key, 1)
            #     elif key_name.find("pliCount") != -1:
            #         inbound_pliCount = preprocess(key, 1)
            #     elif key_name.find("nackCount") != -1:
            #         inbound_nackCount = preprocess(key, 1)
            #     elif key_name.find("qpSum/framesDecoded") != -1:
            #         inbound_qpSum_framesDecoded = preprocess(key, 1)
            #     elif key_name.find("bytesReceived_in_bits/s") != -1:
            #         inbound_bytesReceived_per_sec = preprocess(key, 1)

    with open(output_file_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for index in range(len(remote_inbound_jitter)):
            data = []

            if remote_inbound_jitter != None and index < len(remote_inbound_jitter):
                data.append(round(remote_inbound_jitter[index], 2))
            else:
                data.append("None")

            if remote_packetsLost_per_sec != None and index < len(remote_packetsLost_per_sec):
                if index == 0:
                    data.append(0)
                else:
                    data.append(round(remote_packetsLost_per_sec[index] - remote_packetsLost_per_sec[index-1]))
            else:
                data.append("None")

            if remote_fractionLost != None and index < len(remote_fractionLost):
                data.append(round(remote_fractionLost[index], 2))
            else:
                data.append("None")

            # if inbound_jitter != None and index < len(inbound_jitter):
            #     data.append(inbound_jitter[index])
            # else:
            #     data.append("None")
            #
            # if inbound_packetsLost != None and index < len(inbound_packetsLost):
            #     data.append(inbound_packetsLost[index])
            # else:
            #     data.append("None")
            #
            # if inbound_packetsReceived_per_sec != None and index < len(inbound_packetsReceived_per_sec):
            #     data.append(inbound_packetsReceived_per_sec[index])
            # else:
            #     data.append("None")
            #
            # if inbound_framesReceived_per_sec != None and index < len(inbound_framesReceived_per_sec):
            #     data.append(inbound_framesReceived_per_sec[index])
            # else:
            #     data.append("None")
            #
            # if inbound_frameWidth != None and index < len(inbound_frameWidth):
            #     data.append(inbound_frameWidth[index])
            # else:
            #     data.append("None")
            #
            # if inbound_frameHeight != None and index < len(inbound_frameHeight):
            #     data.append(inbound_frameHeight[index])
            # else:
            #     data.append("None")
            #
            # if inbound_framesPerSecond != None and index < len(inbound_framesPerSecond):
            #     data.append(inbound_framesPerSecond[index])
            # else:
            #     data.append("None")
            #
            # if inbound_framesDropped != None and index < len(inbound_framesDropped):
            #     data.append(inbound_framesDropped[index])
            # else:
            #     data.append("None")
            #
            # if inbound_totalInterFrameDelay_framesDecoded_in_ms != None and index < len(inbound_totalInterFrameDelay_framesDecoded_in_ms):
            #     data.append(inbound_totalInterFrameDelay_framesDecoded_in_ms[index])
            # else:
            #     data.append("None")
            #
            # if inbound_firCount != None and index < len(inbound_firCount):
            #     data.append(inbound_firCount[index])
            # else:
            #     data.append("None")
            #
            # if inbound_pliCount != None and index < len(inbound_pliCount):
            #     data.append(inbound_pliCount[index])
            # else:
            #     data.append("None")
            #
            # if inbound_nackCount != None and index < len(inbound_nackCount):
            #     data.append(inbound_nackCount[index])
            # else:
            #     data.append("None")
            #
            # if inbound_qpSum_framesDecoded != None and index < len(inbound_qpSum_framesDecoded):
            #     data.append(inbound_qpSum_framesDecoded[index])
            # else:
            #     data.append("None")
            #
            # if inbound_bytesReceived_per_sec != None and index < len(inbound_bytesReceived_per_sec):
            #     data.append(inbound_bytesReceived_per_sec[index])
            # else:
            #     data.append("None")

            if outbound_packetsSent_per_sec != None and index < len(outbound_packetsSent_per_sec):
                data.append(round(outbound_packetsSent_per_sec[index]))
            else:
                data.append("None")

            if outbound_frameWidth != None and index < len(outbound_frameWidth):
                data.append(round(outbound_frameWidth[index]))
            else:
                data.append("None")

            if outbound_frameHeight != None and index < len(outbound_frameHeight):
                data.append(round(outbound_frameHeight[index]))
            else:
                data.append("None")

            if outbound_framesPerSecond != None and index < len(outbound_framesPerSecond):
                data.append(round(outbound_framesPerSecond[index]))
            else:
                data.append("None")

            if outbound_framesSent_per_sec != None and index < len(outbound_framesSent_per_sec):
                data.append(round(outbound_framesSent_per_sec[index], 2))
            else:
                data.append("None")

            if outbound_totalPacketSendDelay_packetsSent_in_ms != None and index < len(outbound_totalPacketSendDelay_packetsSent_in_ms):
                data.append(round(outbound_totalPacketSendDelay_packetsSent_in_ms[index]))
            else:
                data.append("None")

            if outbound_firCount_per_sec != None and index < len(outbound_firCount_per_sec):
                if index == 0:
                    data.append(0)
                else:
                    data.append(round(outbound_firCount_per_sec[index] - outbound_firCount_per_sec[index-1]))
            else:
                data.append("None")

            # if outbound_pliCount != None and index < len(outbound_pliCount):
            #     data.append(outbound_pliCount[index])
            # else:
            #     data.append("None")

            if outbound_bytesSent_per_sec != None and index < len(outbound_bytesSent_per_sec):
                data.append(round(outbound_bytesSent_per_sec[index]))
            else:
                data.append("None")

            if outbound_nackCount_per_sec != None and index < len(outbound_nackCount_per_sec):
                if index == 0:
                    data.append(0)
                else:
                    data.append(round(outbound_nackCount_per_sec[index] - outbound_nackCount_per_sec[index-1]))
            else:
                data.append("None")

            if outbound_qpSum_framesEncoded != None and index < len(outbound_qpSum_framesEncoded):
                data.append(round(outbound_qpSum_framesEncoded[index], 2))
            else:
                data.append("None")

            if "None" in data:
                print("Ending parsing since None encountered")
                break

            writer.writerow(data)

    remote_inbound_jitter = None
    remote_packetsLost_per_sec = None
    remote_fractionLost = None

    # inbound_jitter = None
    # inbound_packetsLost = None
    # inbound_packetsReceived_per_sec = None
    # inbound_framesReceived_per_sec = None
    # inbound_frameWidth = None
    # inbound_frameHeight = None
    # inbound_framesPerSecond = None
    # inbound_framesDropped = None
    # inbound_totalInterFrameDelay_framesDecoded_in_ms = None
    # inbound_firCount = None
    # inbound_pliCount = None
    # inbound_nackCount = None
    # inbound_qpSum_framesDecoded = None
    # inbound_bytesReceived_per_sec =  None

    outbound_packetsSent_per_sec = None
    outbound_frameWidth = None
    outbound_frameHeight = None
    outbound_framesPerSecond = None
    outbound_framesSent_per_sec = None
    outbound_totalPacketSendDelay_packetsSent_in_ms = None
    outbound_firCount_per_sec = None
    # outbound_pliCount = None
    outbound_bytesSent_per_sec = None
    outbound_nackCount_per_sec = None
    outbound_qpSum_framesEncoded = None

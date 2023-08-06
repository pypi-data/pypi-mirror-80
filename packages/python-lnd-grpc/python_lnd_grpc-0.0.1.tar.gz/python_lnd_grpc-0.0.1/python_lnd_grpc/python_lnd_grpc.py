# python3
import os
import binascii
import codecs
import grpc
from python_lnd_grpc.lnd_defaults import defaultTLSCertFilename, defaultAdminMacFilename, defaultNetwork, defaultRPCHost, defaultRPCPort
from . import rpc_pb2, rpc_pb2_grpc


lnrpc = rpc_pb2
rpcstub = rpc_pb2_grpc
# TODO: path for for system other than linux
TLS_FILE = os.path.expanduser('~/.lnd/' + defaultTLSCertFilename)
ADMIN_MACAROON_PATH = '~/.lnd/data/chain/bitcoin/'


class Connector(object):
    def __init__(
        self,
        tls_file: str = TLS_FILE,
        macaroon_path: str = ADMIN_MACAROON_PATH,
        macaroon_filename: str = defaultAdminMacFilename,
        network: str = defaultNetwork,
        grpc_host: str = defaultRPCHost,
        grpc_port: str = defaultRPCPort):

        self.full_macaroon_path = os.path.expanduser((macaroon_path + '{}/' + macaroon_filename).format(network))
        with open(TLS_FILE, 'rb') as f:
            self.cert = f.read()
        with open(self.full_macaroon_path, 'rb') as f:
            self.macaroon_bytes = f.read()
            self.macaroon = codecs.encode(self.macaroon_bytes, 'hex')
        self.headers = {'Grpc-Metadata-macaroon': self.macaroon}

    @property
    def _ln_stub(self):
        channel = grpc.secure_channel((defaultRPCHost + ":" + defaultRPCPort), self.combined_credentials)
        return rpcstub.LightningStub(channel)

    @property
    def combined_credentials(self) -> grpc.CallCredentials:
        ssl_creds = grpc.ssl_channel_credentials(self.cert)
        auth_creds = grpc.metadata_call_credentials(self.auth_metadata_plugin)
        return grpc.composite_channel_credentials(ssl_creds, auth_creds)

    def auth_metadata_plugin(self, _, callback):
        callback([("macaroon", self.macaroon)], None)

class LNDMethods(Connector):
    # https://api.lightning.community/#abandonchannel
    def abandon_channel(self, chan_point):
        request = lnrpc.AbandonChannelRequest(
            channel_point = chan_point,
        )
        response = self._ln_stub.AbandonChannel(request)
        return response

    # https://api.lightning.community/#closechannel
    def close_channel(self, chan_point, forcibly, target_confirmation, sat_per_byte_rate, delivery_address_refund):
        request = lnrpc.CloseChannelRequest(
            channel_point=chan_point,
            force=forcibly,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte_rate,
            delivery_address=delivery_address_refund,
        )
        response = self._ln_stub.CloseChannel(request)
        return response

    #async when perm = True
    def connect_peer(self, pubkey: str, host: str, perm: bool = False):
        address = lnrpc.LightningAddress(pubkey=pub_key, host=host)
        request = lnrpc.ConnectPeerRequest(addr = address, perm = perm)
        response = self._ln_stub.ConnectPeer(request)
        return response

    def channel_balance(self):
        response = self._ln_stub.ChannelBalance(lnrpc.ChannelBalanceRequest())
        return response

    def get_info(self):
        response = self._ln_stub.GetInfo(lnrpc.GetInfoRequest())
        return response

    def get_node_info(self, node_id):
        request = lnrpc.NodeInfoRequest(
            pub_key=node_id
        )
        response = self._ln_stub.GetNodeInfo(request)
        return response

    def fee_report(self):
        response = self._ln_stub.FeeReport(lnrpc.FeeReportRequest())
        return response

    def list_channels(self, active, inactive, public, private):
        request = lnrpc.ListChannelsRequest(
            active_only = active,
            inactive_only = inactive,
            public_only = public,
            private_only = private
        )
        response = self._ln_stub.ListChannels(request)
        return response

    def new_address(self):
        response = self._ln_stub.NewAddress(lnrpc.NewAddressRequest())
        return response

    def subscribe_channel_balance(self):
        response = self._ln_stub.SubscribeChannelBackups(lnrpc.ChannelBackupSubscription())
        return response

    def utxos(self):
        response = self.stub.ListUnspent(lnrpc.ListUnspentRequest())
        return response

    def wallet_balance(self):
        response = self._ln_stub.WalletBalance(lnrpc.WalletBalanceRequest()) 
        return response

    '''
    def forwarding_history(self):
        request = lnrpc.ForwardingHistoryRequest(
        start_time=<uint64>,
        end_time=<uint64>,
        index_offset=<uint32>,
        num_max_events=<uint32>,
        )
        response = self.ln_stub.FeeReport(lnrpc.FeeReportRequest())
        return response
    '''
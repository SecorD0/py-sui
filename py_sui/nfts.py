from typing import Optional

import requests

from py_sui.models import Nft


class NFT:
    def __init__(self, client):
        self.client = client
        self.req_get: requests.get = self.client.session.get
        self.req_post: requests.post = self.client.session.post

    def mint(self, nft: Nft) -> Optional[dict]:
        return self.client.transactions.move_call(package_object_id='0x2', module='devnet_nft', function='mint',
                                                  type_arguments=[],
                                                  arguments=[nft.name, nft.description, nft.image_url],
                                                  gas_budget=10_000)

    def mint_example_nft(self) -> Optional[dict]:
        nft = Nft(name='Example NFT', description='An NFT created by Sui Wallet',
                  image_url='ipfs://QmZPWWy5Si54R3d26toaqRiqvCH7HkGdXkxwUgCm2oKKM2?filename=img-sq-01.png')
        return self.mint(nft)

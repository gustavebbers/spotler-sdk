import os

import spotler_sdk

client_key = os.environ["SPOTLER_KEY"]
client_secret = os.environ["SPOTLER_SECRET"]
api_url = "https://restapi.mailplus.nl/integrationservice/"

spotler = spotler_sdk.SDK(api_url, client_key, client_secret)

# ob = spotler.get_contact("gueb02@gmail.com")


# logger.info(spotler.get_contact("gwf48o0b1fw@yahoo.com"))
# spotler.delete_order("0a9fc0ce-01e4-42bf-8d5c-599d65336363")
# order = Order(
#     externalId="2",
#     externalContactId="4de6b91f1ddf49c9c3f7180a3a8f69ef96a7f7eab6b041adaa3489083f1b66fa",
#     date=datetime.now(),
#     value="2000",
#     externalProductIds=["121212"],
# )
# spotler.create_order(order=order)

# prod = spotler.get_product("6624e0af-0e50-4611-9de5-9505ce392dab")
# print(prod)
# spotler.delete_product(prod.externalId)
# prod.externalId = "121212"
prod = spotler.get_product("121212")
prod.brand = "Marge"
spotler.update_product(prod)
print("done")

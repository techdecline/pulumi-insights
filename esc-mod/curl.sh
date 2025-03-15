export PULUMI_ACCESS_TOKEN="<token>"
export organization="pulumi-insights"
export project="vs-subscription"
export environment="vs-subscription"


# Get Environment
curl \
  -H "Accept: application/vnd.pulumi+8" \
  -H "Content-Type: application/json" \
  -H "Authorization: token $PULUMI_ACCESS_TOKEN" \
  --request GET \
  https://api.pulumi.com/api/esc/environments/$organization/$project/$environment

# Append a value to the configuration json

# # Update Environment
# curl \
#   -H "Accept: application/vnd.pulumi+8" \
#   -H "Content-Type: application/json" \
#   -H "Authorization: token $PULUMI_ACCESS_TOKEN" \
#   --request PATCH \
#   --data '{"values":{"vnet-id":"/sub/xxx/vnet"}}' \
#   https://api.pulumi.com/api/esc/environments/$organization/$project/$environment
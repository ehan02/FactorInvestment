class PortfolioConstructor:
    def __init__(self, assets):
        self.assets = assets
       
    def construct_custom_weight(self, weights=None):
        num_assets = len(self.assets)
        if num_assets == 0:
            raise ValueError("Asset list cannot be empty")
        if weights is None:
            weights = {asset: 1 for asset in self.assets}
        if set(weights.keys()) != set(self.assets):
            raise ValueError("Weights dictionary must match the assets.")
        total_weight = sum(weights.values())
        return {asset: w / total_weight for asset, w in weights.items()}
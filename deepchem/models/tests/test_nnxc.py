try:
    from deepchem.models.dft.nnxc import NNLDA
    import torch
    import torch.nn as nn
    from dqc.utils.datastruct import ValGrad, SpinParam
except ModuleNotFoundError:
    raise ModuleNotFoundError("This test requires dqc and torch")


class DummyModel(torch.nn.Module):

    def __init__(self, n):
        super(DummyModel, self).__init__()
        self.linear = nn.Linear(n, 1)

    def forward(self, x):
        return self.linear(x)


def test_nnlda():
    torch.manual_seed(42)
    # It works only for n = 2. Not sure why. Value taken from
    # https://github.com/diffqc/dqc/blob/742eb2576418464609f942def4fb7c3bbdc0cd82/dqc/test/test_xc.py#L15
    n = 2
    model = DummyModel(n)
    k = NNLDA(model, ninpmode=1, outmultmode=1)
    densinfo = ValGrad(
        value=torch.rand((n,), dtype=torch.float32).requires_grad_())
    output = k.get_edensityxc(densinfo).detach()
    expected_output = torch.tensor([0.3386, 0.0177])
    torch.testing.assert_close(output, expected_output, atol=1e-4, rtol=0)

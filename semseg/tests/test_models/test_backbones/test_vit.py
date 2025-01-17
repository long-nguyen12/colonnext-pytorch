import pytest
import torch

from mmseg.models.backbones.vit import VisionTransformer
from .utils import check_norm_state


def test_vit_backbone():
    with pytest.raises(TypeError):
        # pretrained must be a string path
        model = VisionTransformer()
        model.init_weights(pretrained=0)

    with pytest.raises(TypeError):
        # img_size must be int or tuple
        model = VisionTransformer(img_size=512.0)

    with pytest.raises(TypeError):
        # out_indices must be int ,list or tuple
        model = VisionTransformer(out_indices=1.)

    with pytest.raises(TypeError):
        # test upsample_pos_embed function
        x = torch.randn(1, 196)
        VisionTransformer.resize_pos_embed(x, 512, 512, 224, 224, 'bicubic')

    with pytest.raises(RuntimeError):
        # forward inputs must be [N, C, H, W]
        x = torch.randn(3, 30, 30)
        model = VisionTransformer()
        model(x)

    # Test img_size isinstance int
    imgs = torch.randn(1, 3, 224, 224)
    model = VisionTransformer(img_size=224)
    model.init_weights()
    model(imgs)

    # Test norm_eval = True
    model = VisionTransformer(norm_eval=True)
    model.train()

    # Test ViT backbone with input size of 224 and patch size of 16
    model = VisionTransformer()
    model.init_weights()
    model.train()

    assert check_norm_state(model.modules(), True)

    # Test large size input image
    imgs = torch.randn(1, 3, 256, 256)
    feat = model(imgs)
    assert feat[-1].shape == (1, 768, 16, 16)

    # Test small size input image
    imgs = torch.randn(1, 3, 32, 32)
    feat = model(imgs)
    assert feat[-1].shape == (1, 768, 2, 2)

    imgs = torch.randn(1, 3, 224, 224)
    feat = model(imgs)
    assert feat[-1].shape == (1, 768, 14, 14)

    # Test with_cp=True
    model = VisionTransformer(with_cp=True)
    imgs = torch.randn(1, 3, 224, 224)
    feat = model(imgs)
    assert feat[-1].shape == (1, 768, 14, 14)

    # Test with_cls_token=False
    model = VisionTransformer(with_cls_token=False)
    imgs = torch.randn(1, 3, 224, 224)
    feat = model(imgs)
    assert feat[-1].shape == (1, 768, 14, 14)

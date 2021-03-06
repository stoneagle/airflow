package controllers

import (
	"evolution/backend/common/resp"
	"evolution/backend/quant/rpc/engine"

	"github.com/gin-gonic/gin"
)

type Config struct {
	Base
}

func NewConfig() *Config {
	Config := &Config{}
	Config.Prepare()
	return Config
}

func (c *Config) Router(router *gin.RouterGroup) {
	config := router.Group("config")
	config.GET("/type/:asset", c.Type)
	config.GET("/strategy/:ctype", c.Strategy)
	config.GET("/asset", c.Asset)
}

func (c *Config) Type(ctx *gin.Context) {
	asset := ctx.Param("asset")
	atype, err := engine.AssetTypeFromString(asset)
	if err != nil {
		resp.ErrorBusiness(ctx, resp.ErrorEngine, "asset type illegal", err)
		return
	}
	ret, err := c.Rpc.GetType(atype)
	if err != nil {
		resp.ErrorBusiness(ctx, resp.ErrorEngine, "get asset type error", err)
		return
	}
	resp.Success(ctx, ret)
}

func (c *Config) Strategy(ctx *gin.Context) {
	ctype := ctx.Param("ctype")
	ret, err := c.Rpc.GetStrategy(ctype)
	if err != nil {
		resp.ErrorBusiness(ctx, resp.ErrorEngine, "get ctype error", err)
		return
	}
	resp.Success(ctx, ret)
}

func (c *Config) Asset(ctx *gin.Context) {
	asset := map[engine.AssetType]string{
		engine.AssetType_Stock:    "STOCK",
		engine.AssetType_Exchange: "EXCHANGE",
	}
	resp.Success(ctx, asset)
}


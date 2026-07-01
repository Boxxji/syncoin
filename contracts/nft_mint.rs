use anchor_lang::prelude::*;
use anchor_spl::token::{Mint, Token, TokenAccount};

declare_id!("Fg6GsFp2z7Cz4v7e3v5dGq8hQh9UkNJLKpPqRrSsTtUv");

#[program]
pub mod syncoin_nft {
    use super::*;

    /// Mint un NFT de contribution
    pub fn mint_contribution_nft(ctx: Context<MintNFT>, tier: String, metadata_uri: String) -> Result<()> {
        require!(!tier.is_empty() && tier.len() <= 20, NFTError::InvalidTier);
        require!(!metadata_uri.is_empty() && metadata_uri.len() <= 256, NFTError::InvalidMetadata);
        
        let valid_tiers = ["bronze", "silver", "gold", "platinum", "diamond"];
        require!(valid_tiers.contains(&tier.as_str()), NFTError::InvalidTier);
        
        let nft = &mut ctx.accounts.nft;
        let contributor = &ctx.accounts.contributor;
        
        nft.owner = contributor.key();
        nft.tier = tier.clone();
        nft.metadata_uri = metadata_uri.clone();
        nft.minted_at = Clock::get()?.unix_timestamp;
        nft.serial = ctx.accounts.counter.supply + 1;
        
        ctx.accounts.counter.supply += 1;
        
        emit!(NFTMinted {
            owner: contributor.key(),
            tier,
            serial: nft.serial,
            timestamp: nft.minted_at,
        });
        
        Ok(())
    }

    /// Transférer un NFT
    pub fn transfer_nft(ctx: Context<TransferNFT>, new_owner: Pubkey) -> Result<()> {
        let nft = &mut ctx.accounts.nft;
        require!(nft.owner == ctx.accounts.contributor.key(), NFTError::NotOwner);
        
        nft.owner = new_owner;
        
        emit!(NFTTransferred {
            nft_id: ctx.accounts.nft.key(),
            from: ctx.accounts.contributor.key(),
            to: new_owner,
        });
        
        Ok(())
    }

    /// Voir les infos d un NFT
    pub fn view_nft(ctx: Context<ViewNFT>) -> Result<NFTInfo> {
        let nft = &ctx.accounts.nft;
        Ok(NFTInfo {
            owner: nft.owner,
            tier: nft.tier.clone(),
            serial: nft.serial,
            minted_at: nft.minted_at,
            metadata_uri: nft.metadata_uri.clone(),
        })
    }
}

// ─── Structures ──────────────────────────────────────

#[derive(Accounts)]
#[instruction(tier: String, metadata_uri: String)]
pub struct MintNFT<'info> {
    #[account(mut)]
    pub contributor: Signer<'info>,
    #[account(
        init,
        payer = contributor,
        space = 8 + 32 + 20 + 256 + 8 + 8,
        seeds = [b"nft", contributor.key().as_ref(), &[ctx.accounts.counter.supply as u8]],
        bump
    )]
    pub nft: Account<'info, NFT>,
    #[account(mut)]
    pub counter: Account<'info, NFTCounter>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct TransferNFT<'info> {
    #[account(mut)]
    pub contributor: Signer<'info>,
    #[account(mut)]
    pub nft: Account<'info, NFT>,
}

#[derive(Accounts)]
pub struct ViewNFT<'info> {
    pub nft: Account<'info, NFT>,
}

#[account]
pub struct NFT {
    pub owner: Pubkey,
    pub tier: String,        // bronze, silver, gold, platinum, diamond
    pub metadata_uri: String, // URI pointant vers les metadonnees
    pub minted_at: i64,
    pub serial: u64,
}

#[account]
pub struct NFTCounter {
    pub supply: u64,
}

// ─── Events ──────────────────────────────────────────

#[event]
pub struct NFTMinted {
    pub owner: Pubkey,
    pub tier: String,
    pub serial: u64,
    pub timestamp: i64,
}

#[event]
pub struct NFTTransferred {
    pub nft_id: Pubkey,
    pub from: Pubkey,
    pub to: Pubkey,
}

// ─── Info ────────────────────────────────────────────

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct NFTInfo {
    pub owner: Pubkey,
    pub tier: String,
    pub serial: u64,
    pub minted_at: i64,
    pub metadata_uri: String,
}

// ─── Errors ──────────────────────────────────────────

#[error_code]
pub enum NFTError {
    #[msg("Tier invalide. Choisis: bronze, silver, gold, platinum, diamond")]
    InvalidTier,
    #[msg("Metadata URI invalide")]
    InvalidMetadata,
    #[msg("Tu n'es pas le proprietaire de ce NFT")]
    NotOwner,
}

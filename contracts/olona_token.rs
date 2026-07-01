use anchor_lang::prelude::*;
use anchor_spl::token::{self, Mint, Token, TokenAccount, Transfer};

declare_id!("Fg6GsFp2z7Cz4v7e3v5dGq8hQh9UkNJLKpPqRrSsTtUv");

#[program]
pub mod olona_token {
    use super::*;

    /// Distribuer des Olona a un contributeur
    pub fn reward(ctx: Context<Reward>, amount: u64) -> Result<()> {
        require!(amount > 0 && amount <= 1000, OlonaError::InvalidAmount);
        
        let contributor = &ctx.accounts.contributor;
        let olona_mint = &ctx.accounts.olona_mint;
        
        // Verifier que le contributeur a prete du compute
        require!(ctx.accounts.compute_log.compute_shared > 0, OlonaError::NoCompute);
        
        // Minage d Olona (simplifie)
        let olona_amount = amount * 10_u64.pow(olona_mint.decimals as u32);
        
        // Transferer les Olona
        token::mint_to(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                token::MintTo {
                    mint: olona_mint.to_account_info(),
                    to: ctx.accounts.contributor_token.to_account_info(),
                    authority: ctx.accounts.mint_authority.to_account_info(),
                },
            ),
            olona_amount,
        )?;
        
        // Enregistrer la transaction
        let tx = &mut ctx.accounts.transaction;
        tx.contributor = contributor.key();
        tx.amount = olona_amount;
        tx.timestamp = Clock::get()?.unix_timestamp;
        tx.compute_cycles = ctx.accounts.compute_log.compute_shared;
        
        emit!(OlonaRewarded {
            contributor: contributor.key(),
            amount: olona_amount,
            reason: "compute_contribution".to_string(),
        });
        
        Ok(())
    }

    /// Planter un arbre (bruler des Olona)
    pub fn plant_tree(ctx: Context<PlantTree>) -> Result<()> {
        let burn_amount = 50 * 10_u64.pow(ctx.accounts.olona_mint.decimals as u32);
        
        require!(
            ctx.accounts.contributor_token.amount >= burn_amount,
            OlonaError::InsufficientOlona
        );
        
        token::burn(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                token::Burn {
                    mint: ctx.accounts.olona_mint.to_account_info(),
                    from: ctx.accounts.contributor_token.to_account_info(),
                    authority: ctx.accounts.contributor.to_account_info(),
                },
            ),
            burn_amount,
        )?;
        
        emit!(TreePlanted {
            planter: ctx.accounts.contributor.key(),
            olona_burned: burn_amount,
            timestamp: Clock::get()?.unix_timestamp,
        });
        
        Ok(())
    }
}

// ─── Structures ──────────────────────────────────────

#[derive(Accounts)]
pub struct Reward<'info> {
    #[account(mut)]
    pub contributor: Signer<'info>,
    #[account(mut)]
    pub olona_mint: Account<'info, Mint>,
    #[account(mut)]
    pub contributor_token: Account<'info, TokenAccount>,
    pub mint_authority: Signer<'info>,
    #[account(mut)]
    pub compute_log: Account<'info, ComputeLog>,
    #[account(init, payer = contributor, space = 8 + 72)]
    pub transaction: Account<'info, ContributionTransaction>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct PlantTree<'info> {
    #[account(mut)]
    pub contributor: Signer<'info>,
    #[account(mut)]
    pub olona_mint: Account<'info, Mint>,
    #[account(mut)]
    pub contributor_token: Account<'info, TokenAccount>,
    pub token_program: Program<'info, Token>,
}

#[account]
pub struct ComputeLog {
    pub contributor: Pubkey,
    pub compute_shared: u64,
    pub last_contribution: i64,
}

#[account]
pub struct ContributionTransaction {
    pub contributor: Pubkey,
    pub amount: u64,
    pub timestamp: i64,
    pub compute_cycles: u64,
}

// ─── Events ──────────────────────────────────────────

#[event]
pub struct OlonaRewarded {
    pub contributor: Pubkey,
    pub amount: u64,
    pub reason: String,
}

#[event]
pub struct TreePlanted {
    pub planter: Pubkey,
    pub olona_burned: u64,
    pub timestamp: i64,
}

// ─── Errors ──────────────────────────────────────────

#[error_code]
pub enum OlonaError {
    #[msg("Pas assez d'Olona pour planter un arbre")]
    InsufficientOlona,
    #[msg("Montant invalide (1-1000 Olona)")]
    InvalidAmount,
    #[msg("Aucun compute partage, contribuez d'abord")]
    NoCompute,
}

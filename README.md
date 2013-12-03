dissent
=======

Implementation of a decentralized, transferrable, and open software license system using the Bitcoin protocol

### What is this?

This project comes from feelings of mine concerning Valve's Steam system and its related DRM, and for that matter, all DRM sytems. I do not intend to be overly critical, as I own products on multiple platforms described within and as a whole think they do a very good job.

Steam is Valve's video game/software distribution platform. Users can setup an account and then purchase games (or game licenses) and install the software for use on their computer. Quite a few of the titles include the optional DRM aspect which basically verifies that the user does indeed own a legit copy of the game.

In many ways this is an improvement from the old system in which companies either didn't have software protection at all and had their software pirated to the point where Blackbeard himself might blush (Tribes), used CD keys which were easily hacked (Starcraft), or made sure that you had a physical CD in your computer (C&C: Red Alert 2).

Consumers have accepted this new system because digital distribution is convenient and cheap, but there are several losses. Because games are tied to a central account, ultimately that authority has complete control, which can surface in issues such as accounts getting banned and losing hundreds of dollars of games, or some long-term situation where the authority puts in place changes which are even more restrictive to the consumer. Additionally, consumers can lose access if the central network becomes unavailable or the company shuts down the system or goes out of business. One other major aspect is this has more or less killed the reselling of games, which although it was never important for computer games, is relevant to consoles and backlash was seen in Microsoft's short-lived attempt to use such a system for the Xbox One.

Valve has recently made their own strides towards a console-like system with Steam on Linux, which is exciting because it could finally eliminate the "Microsoft tax" that computer gamers pay, and allow much needed openness in the console space. However, I have major concerns that even though Valve has mostly been a benevolent dictator, they would very quickly become a monopoly in the space, and monopolies long-term limit innovation.

Such a problem is not limited to just Valve. EA has their own DRM/distribution platform, with the same issues. Companies are incentivized to design their own systems because they are able to have control. It is even less convenient for the consumer, because they now have to manage multiple clients for their library of games. Additionally, because these systems aren't open, there is no way to make a better client.

Such systems are also widespread across other digital goods such as books and music.

In light of this, I would like to propose a form of DRM which uses the Bitcoin protocol and derived cryptocurrencies and is decentralized (does not rely on a central authority for authentication), transferrable (allows resell of goods), and open (is not properietary and locked-in).

### Warning

A lot of what I just wrote is idealism, and I will freely admit that I am ignorant on the certain specific details of implementation and whether such an approach is actually workable. More than anything this work is an attempt to generate discusion and see what actually is possible.

### Details

When looking at Bitcoin, what most people see is the rampant speculation. However, the protocol itself has really interesting technical properties which make it useful for a lot more than just a form of currency. Its main useful property is that all transactions are available to everyone else and such transactions are verified throughout the network, making it both transparent and secure.

One of the uses of the network that I have run across is "ownership of property", which allows the transfer of items such as ownership of a vehicle. A very good description can be found here:

http://frozenlock.files.wordpress.com/2011/11/master-bitcoin.pdf

I strongly suggest that you read it, especially if my description is lacking. One other, shorter, much less technical description is found here:

http://www.reddit.com/r/Bitcoin/comments/1o3f21/proof_of_ownership_for_real_life_items_backed_by/

The former mentions software keys but does not go into detail how that would work in relation to DRM. A short description is as follows:

A company wants to sell keys to their game. To do this they create a "master" address (M) that is specific to the game. When a user purchases a copy of the game, they then transfer a balance from the master to an address specific to the user (U) [1]. How large this balance is does not matter, all that matters is some amount was transferred from one address to the other, the transaction itself confers ownership [2].

At this point, the user can now either transfer their ownership to someone else (resell) [3] or to a different address of their own [4]. The important point is that all such transfers because they use the Bitcoin protocol are verifiable by anyone with a copy of the global blockchain.

[1] M1.send(U1, 1.0)

[2] M1.send(U1, .01)

[3] M1.send(U1, 1.0), U1.send(U2, 1.0)

[4] M1.send(U1, 1.0), U1.send(U1a, 1.0)

If you want to use this in terms of DRM, all that is necessary is for a piece of software to confirm that the user owns an address which has a balance which at some point in the past originated from the master address specific to the software.

Some small technicalities have easy fixes.

What keeps a user from transferring to multiple accounts and transferring ownership to multiple people? When the majority of a balance is transferred, so is ownership.

M1.send(U1, 1.0), U1.send(U2, .4), U1.send(U3, .6)

U3 has ownership.

When half of a balance is transferred, ownership is conferred by the first transaction.

M1.send(U1, 1.0), U1.send(U2, .5), U1.send(U3, .5)

U2 has ownership.

Note: Some uses might find it worthwhile to actually have divisible ownership, but that is not wanted in this case.

### Implementation

Now, having discussed Bitcoin, the actual implementation uses Namecoin. Namecoin is almost identical to Bitcoin, but has the additional feature that each coin amount can serve as a key/value store, and was originally envisioned as a distributed DNS. Namecoin is not required, but I use it because it has a local API which makes it very easy to get a history of addresses/transactions external to your local wallet, which I could not easily do with Bitcoin. 

I want to restate that Namecoin is just an implementation detail, such an approach should work on any crytocurrency with the right tools and slight modifications.

Namecoin allows you to pay a small amount of Namecoin to register unique names. Once you own that name, you can pay a small transaction fee to update it, and you can transfer ownership of it. So, only one person can own 'hi', or 'name' or 'd/reddit' at a time.

In terms of the digital rights sytem I am discussing, this adds the requirement that for a company to create and transfer a software key, they have to create a unique Namecoin name for each copy. In this situation, the master address is:

N3FDuSqd4FHZ6DSZtXJgNGr3Tyq4ni8CFL

The first name I created is 'here-is-a-test' and you can see the history here: http://explorer.dot-bit.org/n/125436.

Here's how it works.

1) When the program starts, it asks you for the unique global name. This is saved after the first run.

2) It verifies that the name did at some point originate from the master address.

3) It attempts to create a new address and transfers ownership to that address. Why? This verifies that you have ownership of the name, and it also locks down use to one copy of the program at a time.

4) Now the actual program part runs, which just echoes whatever you type in, but in the background is a repeating 10 minute check which makes sure that there has not been another transaction involving the name, if there has, we can assume that either ownership has been transferred to someone else, or more often, another copy of the program has been started. If a transaction has occurred, your copy shuts down.

In principle, we now have a working, decentralized, transferrable, and open DRM system.

### How to run it

You need:

1) Python (only tested on 2.7)

2) https://github.com/jgarzik/python-bitcoinrpc 

3) Namecoin-Qt

4) A key tranferred from the master address to yours, though you can do your own testing with some very simple changes of the code.

Once you have all that downloaded and setup, you need to run:

namecoin-qt -server -rpcuser=user -rpcpassword=password

Once the entire blockchain is downloaded (could take a few hours), run the actual script....

python dissent.py

### Current issues and future possibilities

I hope I have made it clear that I am ignorant on current systems and as such something like this might not work at all because it would get hacked way too quickly.

It is worth noting that no copy protection is perfect and to my knowledge even Steam games end up stripped of their protection and pirated. Essentially what you are looking for is something that is convenient and just good enough to keep the honest people honest.

I'm thinking for a real system based around this concept to work, you'd want your Bitcoin/Namecoin/whatever client to function as your 'Steam' application and to somehow keep the local blockchain accurate and protected. What I don't know is if that is even realistic, especially with an open system.

Some interesting possibilties are companies no longer being stuck in a centralized marketplace or having to give up a cut, but simply selling their keys using their own websites (not entirely unlike how you can buy Steam keys from third-parties currently). Returns are trivial in such a system. Unsatisfied? You could transfer your balance back within 48 hours. Sales numbers become easy to track. Both company and consumer would have proof of sale. And since you are already working with the tech, maybe accepting payments in Bitcoin or whatever is more likely.

Other possibilties include a global catalog of softwar/prices/related information distribut4ed on a Namecoin-esque system or in-game trophies/achievements distributed in the same manner as ownership.

Instead of proprietary, closed, limited clients open software could be developed which any company could base their client upon, and of course users could use that client and the assocated features or use open ones.

I did run into some difficulties inherent to the protocol itself:

1) Each transaction requires a fee, which is not a huge problem when actually transferring ownership (you can easily transfer a small amount into your address to reload your balance), but by having a transaction everytime the program starts you quickily start talking about costs you don't want.

This is not just an issue with Namecoin, Bitcoin has one, too. Such a fee is understandable, it prevents people from flooding the network with junk transactions and for some cryptos inventivizes miners, but it limits what is possible. Do any cryptos exist which don't have a transaction fee? Could such a thing exist? With fees, microtransactions can be difficult which seem to be a rather large aea of need.... 

I wonder if Peercoin wouldn't make a great base, with its inherent inflation (perhaps important because users would be incentivized to hoard parts of currency matching to product ownership) and its use of proof of stake implying increased long-term security and energy savings. Peercoin itself has even higher transaction fees inherent to its purpose, but it
 could be worth consideration.
 
2) Namecoin only allows a transaction to happen once the last transaction involving the name has at least one confirmation, which makes sense, but means that if say your game shut down and you needed to restart it, it could take 5-30 minutes to wait for the last transaction to clear before you could start the game. Obviously not okay from a user's point of view.

3) If you used Namecoin as a base, you could quickly run out of globally unique names due to each software key needing one. Namecoin also has the concept of expiry which I ignore in this project. A final issue is that obtaining a name requires registration which can take anywhere from a few hours to a day, which doesn't work for instant access.

Interestingly, a cryptocurrency which allowed this would have an added benefit that it would have "real" value backing it, which is something that is debated and argued about.

### What's in a name?

I recently watched Manufacturing Consent about Noam Chomsky. I'm not trying to advocate the man or his ideas,  dissent is a play on decentralized.

## Contact

If you are interested in this project (or the idea of a cryto better suited for microtransactions or development) at all or would like to provide feedback of any kind, either create a new issue here on Github (https://github.com/aaron-lebo/dissent/issues) or shoot me an email:

Aaron dot M dot Lebo at gmail dot com

I really, really want to hear from people, if such a system is at all feasible I want to help make it happen.

I want to thank the kind anonymous soul who donated 1 Namecoin on #namecoin several nights back. You made this possible. 
Below are a few of my addresses for different cryptos, if you would like to tip a few cents, I would be very grateful.

114nsPGhJ9wN8QoA4RDGvgrouR9M8xi43V

LccGuFx4T7Kwyt6LGHCYFTWSoyXPhiNW4v

PCEarGJWko7WDr4YwudtZyXfpykBmHqU2F

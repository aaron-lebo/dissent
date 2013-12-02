dissent
=======
## What is this?

This project comes from feelings of mine concerning Valve's Steam system and its related DRM.

Just to inform those who are not aware of what that is, Steam is Valve's video game/software distribution platform. Users can setup an account and then purchase games (or game licenses) and install the software for use on their computer. Quite a few of the titles include the optional DRM aspect which basically verifies that the user does indeed own a legit copy of the game.

In many ways this is an improvement from the old system in which companies either didn't have software protection at all and had their software pirated like crazy, used CD keys which were easily hacked, or made sure that you had a physical CD in your computer.

Consumers have accepted this system because digital distribution is convenient and cheap, but there are several losses for the consumer. Because games are tied to a Valve account, ultimately Valve has complete control, which can surface in issues such as accounts getting banned (although infrequently) and losing hundreds of dollars of games, or some long-term situation where Valve puts in place changes which are even more restrictive to the consumer. One other major aspect is this has more or less killed the reselling of games, which although was never important for computer games, is relevant to consoles and backlash was seen in Microsoft's short-lived attempts to use such a system for their Xbox One.

Valve has recently made their own strides towards a console-like system with Steam on Linux, which is exciting because it could finally eliminate the "Microsoft tax" that computer gamers pay, and allow much needed openness in the console space. However, I have major concerns that even though Valve has mostly been a benevolent dictator, they would very quickly because a monopoly in the space, and monopolies long-term limit innovation.

Such a problem is not limited to just Valve. EA has their own DRM/distribution platform, which can be pretty inconvenient when you need to open up two different clients to manage your library of games. Additionally, because these systems aren't open, there is no way to make a better client, or a client which ties together different systems.

Of course such systems are also widespread across other digital goods such as books and music.

In light of this, I would like to propose a form of DRM which using the Bitcoin protocol and derived cryptocurrencies is decentralized, transferrable, and open.

### Warning

A lot of what I just wrote is idealism, and I will admit freely that I am very ignorant on the actually specific details of implementation and whether such an approach is actually workable. More than anything this work is an attempt to generate discusion and see what actually is possible.

### Details

When looking at Bitcoin, what most people see is the rampant speculation. However, the protocol itself has really interesting technical properties which make it useful for a lot more than just a form of currency. Its main useful property is that all transactions are available to everyone else and such transactions are verified throughout the network, making it both transparent and secure.

One of the uses of the network that I have run across is "ownership of property", which allows the transfer of items such as ownership of a vehicle. I feel like the very best item I have read on the topic is:

http://frozenlock.files.wordpress.com/2011/11/master-bitcoin.pdf

The author mentions software keys but does not go into detail how that would work in relation to DRM. A short description is as follows:

A company wants to sell keys to their game. To do this they create a "master" address (M) that is specific to the game. When a user purchases a copy of the game, they then transfer a balance from this address to an address specific to the user (U) [1]. How large this balance is does not matter, all that matters is some amount was transferred from one address to the other, the transaction itself confers ownership [2].

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

Now, having discussed Bitcoin, the actual implementation uses Namecoin. Namecoin is almost identical to Bitcoin, but has the additional feature that each coin amount can serve as a key/value store, and was originally envisioned as a distributed DNS. Namecoin is not required, but I use it because it has a local API which makes it very easy to get a history of transactions outside of your wallet local to your machine, which I could not easily do with Bitcoin.  

Namecoin allows you to pay a small amount of Namecoin to register unique names. Once you own that name, you can pay a small transaction fee to update it, and you can transfer ownership of it. So, only one person can own 'hi', or 'name' or 'd/name' at a time.

In terms of the digital rights sytem I am discussing, this adds the requirement that for a company to create and transfer a software key, they have to create a unique Namecoin name for each copy. In this situation, the master address is:

N3FDuSqd4FHZ6DSZtXJgNGr3Tyq4ni8CFL

The first name I created is 'here-is-a-test' and you can see the history here: http://explorer.dot-bit.org/n/125436.

Here's how it works.

1) When the program starts, it asks you for the master address, and the name.

2) It verifies that the name did at some point originate from the master address.

3) It attempts to create a new address and transfers ownership to that address. Why? This verifies that you have ownership of the name, and it also locks down use to one copy of the program at a time.

4) Now the actual program part runs, which just repeats whatever you type in, but in the background is a repeating 10 minute check which makes sure that there has not been another transaction involving the name, if there has, we can assume that either ownership has been transferred to someone else, or more often, another copy of the program has been started. If a transaction has occurred, your copy shuts down.

In principle, we now have a working, decentralized, transferrable, and open DRM system, not to mention one that does not require someone else's servers to work for you to play your game.

### How to run

You need:

1) Python (only tested on 2.7)

2) https://github.com/jgarzik/python-bitcoinrpc 

3) Namecoin-Qt

4) A key tranferred from the master address to yours, though you can do your own testing with some very simple changes of the code.

Once you have all that downloaded and setup, you need to run:

namecoin-qt -server -rpcuser=user -rpcpassword=password

and then run the actual script....

python dissent.py

### Current issues and future possibilities

I hope I have made it clear that I am pretty damn igorant on current systems and as such something like this might not work at all because it would get hacked within seconds.

It is worth noting that no copy protection is perefect and to my knowledge even Steam games end up stripped of their protection and pirated. Essentially what you are looking for is something that is convenient and just good enough to keep the honest people honest.

I'm thinking for a real system based around this concept to work, you'd want your Bitcoin/Namecoin/whatever client to function as your 'Steam' application and to somehow keep the local blockchain accurate and protected. What I don't know is if that is even realistic, especially with an open system.

Some interesting possibilties are companies no longer being stuck in a centralized marketplace or have to give up a cut, but simply sell their keys using their own websites (not entirely unlike how you can buy Steam keys from third-parties currently). Returns are trivial in such a system. Unsatisfied? You could transfer your balance back within 48 hours. Sales numbers become easy to track. Both company and consumer would have proof of sale. And since you are already working with the tech, maybe accepting payments in Bitcoin or whatever is more likely.

Instead of proprietary, closed, limited clients open software could be developed which any company could base their client upon, and of course users could use that client and the assocated features or use open ones.

I did run into some difficulties inherent to the protocol itself:

1) Each transaction requires a fee, which is not a huge problem when actually transferring ownership (you can easily transfer a small amount into your address to reload your balance), but by having a transaction everytime the program starts you quickily start talking about costs you don't want.
This is not just an issue with Namecoin, Bitcoin has one, too. Such a fee is understandable, it prevents people from flooding the network with junk transactions and for some cryptos inventivizes miners, but it limits what is possible. Do any cryptos exist which don't have a transaction fee? Could such a thing exist? With fees, microtransactions can be difficult which seem to be a rather large aea of need.... 
2) Namecoin only allows a transaction to happen once the last transaction involving the name has at least one confirmation, which makes sense, but means that if say your game shut down and you needed to restart it, it could take 5-30 minutes to wait for the last transaction to clear before you could start the game. Obviously not okay from a user's point of view.
